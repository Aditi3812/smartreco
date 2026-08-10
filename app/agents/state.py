from typing import Any, TypedDict


class RecommendationState(TypedDict, total=False):

    # -----------------------------------------
    # User
    # -----------------------------------------

    user_id: int

    # -----------------------------------------
    # User context
    # -----------------------------------------
    db: Any
    behavior_profile: Any
    interactions: list[Any]
    top_products: list[Any]
    behavior_summary: dict
    # -----------------------------------------
    # Retrieval
    # -----------------------------------------
    
    semantic_results: list[Any]
    # -----------------------------------------
    # Recommendation candidates
    # -----------------------------------------

    candidates: list[dict[str, Any]]

    ranked_recommendations: list[dict[str, Any]]
    # -----------------------------------------
    # Hybrid ranking
    # -----------------------------------------

    ranked_candidates: list[dict[str, Any]]

    final_recommendations: list[dict[str, Any]]
    
    # -----------------------------------------
    # Agent output
    # -----------------------------------------

    explanations: list[str]

    # -----------------------------------------
    # Control
    # -----------------------------------------

    limit: int

    error: str | None