
from langgraph.graph import StateGraph, START, END

from app.agents.state import RecommendationState

from app.database.database import SessionLocal

from app.repositories.behavior_profile_repository import (
    behavior_profile_repository,
)

from app.repositories.product_interaction_repository import (
    product_interaction_repository,
)

from app.services.semantic_retrieval_service import (
    semantic_retrieval_service,
)

from app.services.hybrid_ranking_service import (
    hybrid_ranking_service,
)

from app.models.product import Product


# =========================================================
# 1. COLLECT USER CONTEXT
# =========================================================

def collect_context(
    state: RecommendationState,
):

    user_id = state["user_id"]

    # Create a database session for this node
    db = SessionLocal()

    try:

        # -----------------------------------------
        # 1. Get behavior profile
        # -----------------------------------------

        behavior_profile = (
            behavior_profile_repository
            .get_by_user_id(
                db,
                user_id,
            )
        )

        # -----------------------------------------
        # 2. Get product interactions
        # -----------------------------------------

        interactions = (
            product_interaction_repository
            .get_by_user(
                db,
                user_id,
            )
        )

        # -----------------------------------------
        # 3. Get top interacted products
        # -----------------------------------------

        top_products = interactions[:5]

        return {
            "behavior_profile": behavior_profile,
            "interactions": interactions,
            "top_products": top_products,
        }

    finally:

        db.close()


# =========================================================
# 2. ANALYZE BEHAVIOR
# =========================================================

def analyze_behavior(
    state: RecommendationState,
):

    behavior_profile = state.get(
        "behavior_profile"
    )

    # -----------------------------------------
    # No behavior profile
    # -----------------------------------------

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

    # -----------------------------------------
    # Category interests
    # -----------------------------------------

    category_scores = (
        behavior_profile.category_scores
        or {}
    )

    top_categories = sorted(
        category_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:5]

    # -----------------------------------------
    # Difficulty interests
    # -----------------------------------------

    difficulty_scores = (
        behavior_profile.difficulty_scores
        or {}
    )

    top_difficulties = sorted(
        difficulty_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:3]

    # -----------------------------------------
    # Language interests
    # -----------------------------------------

    language_scores = (
        behavior_profile.language_scores
        or {}
    )

    top_languages = sorted(
        language_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:3]

    # -----------------------------------------
    # Build behavioral interpretation
    # -----------------------------------------

    behavior_summary = {

        "top_categories": top_categories,

        "top_difficulties": top_difficulties,

        "top_languages": top_languages,

        "purchase_intent": (
            behavior_profile.purchase_intent
            or 0.0
        ),

        "search_frequency": (
            behavior_profile.search_frequency
            or 0.0
        ),

        "average_time_spent": (
            behavior_profile.average_time_spent
            or 0.0
        ),

        "average_scroll_depth": (
            behavior_profile.average_scroll_depth
            or 0.0
        ),

        "total_events": (
            behavior_profile.total_events
            or 0
        ),
    }

    return {
        "behavior_summary": behavior_summary
    }


# =========================================================
# 3. SEMANTIC RETRIEVAL
# =========================================================

def semantic_retrieval(
    state: RecommendationState,
):

    user_id = state["user_id"]

    behavior_profile = state.get(
        "behavior_profile"
    )

    top_products = state.get(
        "top_products",
        [],
    )

    db = SessionLocal()

    try:

        semantic_data = (
            semantic_retrieval_service
            .retrieve_for_user(
                db,
                user_id,
                behavior_profile,
                top_products,
                limit=10,
            )
        )

        return {
            "semantic_results": (
                semantic_data.get(
                    "results",
                    []
                )
            ),
        }

    finally:

        db.close()


# =========================================================
# 4. BUILD RECOMMENDATION CANDIDATES
# =========================================================

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

            # -----------------------------------------
            # Extract product ID from Qdrant payload
            # -----------------------------------------

            payload = result.payload or {}

            product_id = payload.get(
                "product_id"
            )

            # -----------------------------------------
            # Skip malformed results
            # -----------------------------------------

            if not product_id:
                continue

            # -----------------------------------------
            # Extract semantic similarity score
            # -----------------------------------------

            semantic_score = float(
                result.score
            )

            # -----------------------------------------
            # Fetch complete product from PostgreSQL
            # -----------------------------------------

            product = (
                db.query(Product)
                .filter(
                    Product.id == product_id
                )
                .first()
            )

            if not product:
                continue

            # -----------------------------------------
            # Build candidate
            # -----------------------------------------

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


# =========================================================
# 5. HYBRID RANKING
# =========================================================
def hybrid_rank(
    state: RecommendationState,
):

    candidates = state.get(
        "candidates",
        [],
    )

    behavior_profile = state.get(
        "behavior_profile"
    )

    interactions = state.get(
        "interactions",
        [],
    )

    # -----------------------------------------
    # No behavior profile
    # -----------------------------------------

    if not behavior_profile:
        return {
            "ranked_recommendations": []
        }

    # -----------------------------------------
    # Hybrid ranking
    # -----------------------------------------

    ranked = (
        hybrid_ranking_service
        .rank_candidates(
            candidates,
            behavior_profile,
            interactions,
        )
    )

    # -----------------------------------------
    # Recommendation limit
    # -----------------------------------------

    limit = state.get(
        "limit",
        5,
    )

    return {
        "ranked_recommendations": (
            ranked[:limit]
        )
    }

# =========================================================
# 6. BUILD LANGGRAPH AGENT
# =========================================================

def build_recommendation_agent():

    graph = StateGraph(
        RecommendationState
    )

    # =====================================================
    # Nodes
    # =====================================================

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

    # =====================================================
    # Edges
    # =====================================================

    graph.add_edge(
        START,
        "collect_context",
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
        END,
    )

    # =====================================================
    # Compile
    # =====================================================

    return graph.compile()


# =========================================================
# 7. CREATE AGENT
# =========================================================

recommendation_agent = (
    build_recommendation_agent()
)

