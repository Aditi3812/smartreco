#MAIN AGENTIC WORKFLOW VIA LANGGRAPH:
from app.services.recommendation_trigger_service import (
    recommendation_trigger_service,
)
from app.repositories.recommendation_repository import (
    recommendation_repository,
)
from langgraph.graph import StateGraph, START, END
from app.agents.state import RecommendationState
from app.database.database import SessionLocal
from app.repositories.behavior_profile_repository import (
    behavior_profile_repository,
)
from app.repositories.product_interaction_repository import (
    product_interaction_repository,
)
from app.repositories.event_repository import (
    event_repository,
)
from app.services.behavior_profile_service import (
    behavior_profile_service,
)
from app.services.semantic_retrieval_service import (
    semantic_retrieval_service,
)
from app.services.hybrid_ranking_service import (
    hybrid_ranking_service,
)
from app.services.recommendation_generation_service import (
    recommendation_generation_service,
)
from app.models.product import Product
from app.repositories.product_repository import product_repository


def check_recommendation_trigger(
    state: RecommendationState,
):
    user_id = state["user_id"]
    db = SessionLocal()
    try:
        should_generate = (
            recommendation_trigger_service.should_generate(
                db,
                user_id,
            )
        )
        return {
            "should_generate": should_generate,
        }
    finally:
        db.close()

def collect_context(
    state: RecommendationState,
):
    user_id = state["user_id"]
    db = SessionLocal()
    try:
        # 1. Get Behavior Profile (Build automatically if user has events but no profile row)
        behavior_profile = behavior_profile_repository.get_by_user_id(
            db,
            user_id,
        )

        if not behavior_profile:
            user_events = event_repository.get_by_user_id(db, user_id)
            if user_events:
                behavior_profile = behavior_profile_service.build_profile(
                    db,
                    user_id,
                )

        # 2. Get Aggregated Product Interactions
        interactions = product_interaction_repository.get_by_user(
            db,
            user_id,
        )

        # 3. Top products context
        top_products = interactions[:5] if interactions else []

        return {
            "behavior_profile": behavior_profile,
            "interactions": interactions,
            "top_products": top_products,
        }
    finally:
        db.close()


def route_after_trigger(
    state: RecommendationState,
):
    if state.get(
        "should_generate",
        True,
    ):
        return "generate"
    return "reuse"


def reuse_existing_recommendation(state: RecommendationState):
    user_id = state["user_id"]
    db = SessionLocal()
    try:
        latest = recommendation_repository.get_latest_for_user(
            db,
            user_id,
            limit=1,
        )
        if not latest:
            return {"ai_recommendation": None}
        rec = latest[0]
        product = product_repository.get_by_id(db, rec.product_id)
        title = product.title if product else f"Product #{rec.product_id}"
        return {
            "ai_recommendation": {
                "product_id": rec.product_id,
                "title": title,
                "reason": f"Cached recommendation (Rank #{rec.rank} with final hybrid score of {rec.final_score:.4f})",
                "confidence": round(rec.final_score, 4),
            }
        }
    finally:
        db.close()


def analyze_behavior(
    state: RecommendationState,
):
    behavior_profile = state.get("behavior_profile")
    if not behavior_profile:
        return {
            "behavior_summary": {
                "top_categories": [],
                "top_difficulties": [],
                "top_languages": [],
                "purchase_intent": 0.0,
                "search_frequency": 0.0,
                "average_time_spent": 0.0,
                "average_scroll_depth": 0.0,
                "total_events": 0,
            }
        }
    category_scores = behavior_profile.category_scores or {}
    top_categories = sorted(
        category_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:5]
    difficulty_scores = behavior_profile.difficulty_scores or {}
    top_difficulties = sorted(
        difficulty_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:3]
    language_scores = behavior_profile.language_scores or {}
    top_languages = sorted(
        language_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:3]
    behavior_summary = {
        "top_categories": top_categories,
        "top_difficulties": top_difficulties,
        "top_languages": top_languages,
        "purchase_intent": (behavior_profile.purchase_intent or 0.0),
        "search_frequency": (behavior_profile.search_frequency or 0.0),
        "average_time_spent": (behavior_profile.average_time_spent or 0.0),
        "average_scroll_depth": (behavior_profile.average_scroll_depth or 0.0),
        "total_events": (behavior_profile.total_events or 0),
    }
    return {"behavior_summary": behavior_summary}


def semantic_retrieval(
    state: RecommendationState,
):
    user_id = state["user_id"]
    behavior_profile = state.get("behavior_profile")
    top_products = state.get(
        "top_products",
        [],
    )
    db = SessionLocal()
    try:
        semantic_data = semantic_retrieval_service.retrieve_for_user(
            db,
            user_id,
            behavior_profile,
            top_products,
            limit=10,
        )
        return {
            "semantic_results": (semantic_data.get("results", [])),
        }
    finally:
        db.close()


def build_candidates(
    state: RecommendationState,
):
    semantic_results = state.get(
        "semantic_results",
        [],
    )
    candidates = []
    db = SessionLocal()
    try:
        for result in semantic_results:
            if isinstance(result, dict):
                product = result.get("product")
                semantic_score = float(
                    result.get(
                        "semantic_score",
                        0.0,
                    )
                )
                if not product:
                    continue
                candidates.append(
                    {
                        "product": product,
                        "semantic_score": semantic_score,
                    }
                )
                continue
            payload = result.payload or {}
            product_id = payload.get("product_id")
            if not product_id:
                continue
            semantic_score = float(result.score)
            product = (
                db.query(Product).filter(Product.id == product_id).first()
            )
            if not product:
                continue
            candidates.append(
                {
                    "product": product,
                    "semantic_score": semantic_score,
                }
            )
        return {
            "candidates": candidates,
        }
    finally:
        db.close()


def hybrid_rank(
    state: RecommendationState,
):
    candidates = state.get(
        "candidates",
        [],
    )
    behavior_profile = state.get("behavior_profile")
    interactions = state.get(
        "interactions",
        [],
    )
    limit = state.get(
        "limit",
        5,
    )
    if not behavior_profile:
        ranked = []
        for candidate in candidates:
            product = candidate["product"]
            semantic_score = candidate.get(
                "semantic_score",
                0.0,
            )
            behavioral_score = 0.0
            preference_score = 0.0
            final_score = round(
                semantic_score,
                4,
            )
            ranked.append(
                {
                    "product": product,
                    "behavioral_score": behavioral_score,
                    "semantic_score": semantic_score,
                    "preference_score": preference_score,
                    "final_score": final_score,
                }
            )
        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True,
        )
        return {"ranked_recommendations": (ranked[:limit])}

    ranked = hybrid_ranking_service.rank_candidates(
        candidates,
        behavior_profile,
        interactions,
    )
    return {"ranked_recommendations": (ranked[:limit])}


def generate_ai_recommendation(
    state: RecommendationState,
):
    ranked = state.get(
        "ranked_recommendations",
        [],
    )
    behavior = state.get(
        "behavior_summary",
        {},
    )
    result = recommendation_generation_service.generate(
        ranked,
        behavior,
    )
    return {"ai_recommendation": result}


def build_recommendation_agent():
    graph = StateGraph(RecommendationState)
    graph.add_node(
        "check_recommendation_trigger",
        check_recommendation_trigger,
    )
    graph.add_node(
        "reuse_existing_recommendation",
        reuse_existing_recommendation,
    )
    graph.add_node(
        "collect_context",
        collect_context,
    )
    graph.add_node(
        "analyze_behavior",
        analyze_behavior,
    )
    graph.add_node(
        "semantic_retrieval",
        semantic_retrieval,
    )
    graph.add_node(
        "build_candidates",
        build_candidates,
    )
    graph.add_node(
        "hybrid_rank",
        hybrid_rank,
    )
    graph.add_node(
        "generate_ai_recommendation",
        generate_ai_recommendation,
    )
    graph.add_edge(
        START,
        "check_recommendation_trigger",
    )
    graph.add_conditional_edges(
        "check_recommendation_trigger",
        route_after_trigger,
        {
            "generate": "collect_context",
            "reuse": "reuse_existing_recommendation",
        },
    )
    graph.add_edge(
        "reuse_existing_recommendation",
        END,
    )
    graph.add_edge(
        "collect_context",
        "analyze_behavior",
    )
    graph.add_edge(
        "analyze_behavior",
        "semantic_retrieval",
    )
    graph.add_edge(
        "semantic_retrieval",
        "build_candidates",
    )
    graph.add_edge(
        "build_candidates",
        "hybrid_rank",
    )
    graph.add_edge(
        "hybrid_rank",
        "generate_ai_recommendation",
    )
    graph.add_edge(
        "generate_ai_recommendation",
        END,
    )
    return graph.compile()


recommendation_agent_v2 = build_recommendation_agent()