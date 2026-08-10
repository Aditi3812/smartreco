from app.models.recommendation import Recommendation

from app.repositories.recommendation_repository import (
    recommendation_repository,
)

from app.repositories.recommendation_repository import (
    recommendation_repository,
)
from app.repositories.behavior_profile_repository import (
    behavior_profile_repository,
)

from app.repositories.product_interaction_repository import (
    product_interaction_repository,
)

from app.repositories.product_repository import (
    product_repository,
)

from app.services.semantic_retrieval_service import (
    semantic_retrieval_service,
)

from app.services.hybrid_ranking_service import (
    hybrid_ranking_service,
)


class RecommendationService:
    """
    Orchestrates the complete recommendation pipeline.
    """

    def generate_recommendations(
        self,
        db,
        user_id: int,
        limit: int = 5,
    ):

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

        if not behavior_profile:
            return []

        # -----------------------------------------
        # 2. Get user interactions
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

        # -----------------------------------------
        # 4. Semantic retrieval
        # -----------------------------------------

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

        semantic_results = (
            semantic_data["results"]
        )

        # -----------------------------------------
        # 5. Build semantic score lookup
        # -----------------------------------------

        semantic_scores = {
            result.payload["product_id"]:
                result.score
            for result in semantic_results
        }

        # -----------------------------------------
        # 6. Behavioral score lookup
        # -----------------------------------------

        behavioral_scores = {
            interaction.product_id:
                interaction.final_score
            for interaction in interactions
        }

        # -----------------------------------------
        # 7. Get all products
        # -----------------------------------------

        products = (
            product_repository
            .get_all(
                db
            )
        )

        # -----------------------------------------
        # 8. Identify purchased products
        # -----------------------------------------

        purchased_ids = set()

        for interaction in interactions:

            # Purchase information will be
            # handled properly once PURCHASE
            # events are connected to interactions.

            if getattr(
                interaction,
                "purchased",
                False,
            ):
                purchased_ids.add(
                    interaction.product_id
                )

        # -----------------------------------------
        # 9. Build candidates
        # -----------------------------------------

        candidates = []

        for product in products:

            # Never recommend purchased products
            if product.id in purchased_ids:
                continue

            candidates.append(
                {
                    "product": product,
                    "behavioral_score":
                        behavioral_scores.get(
                            product.id,
                            0.0,
                        ),
                    "semantic_score":
                        semantic_scores.get(
                            product.id,
                            0.0,
                        ),
                }
            )

        # -----------------------------------------
        # 10. Hybrid ranking
        # -----------------------------------------

        ranked = (
            hybrid_ranking_service
            .rank_candidates(
                candidates,
                behavior_profile,
            )
        )

        # -----------------------------------------
        # 11. Get top N recommendations
        # -----------------------------------------

        top_ranked = ranked[:limit]

        # -----------------------------------------
        # 12. Store recommendations
        # -----------------------------------------

        for rank, item in enumerate(
            top_ranked,
            start=1,
        ):

            recommendation = Recommendation(
                user_id=user_id,
                product_id=item["product"].id,
                rank=rank,
                behavioral_score=item["behavioral_score"],
                semantic_score=item["semantic_score"],
                preference_score=item["preference_score"],
                final_score=item["final_score"],
            )

            recommendation_repository.create(
                db,
                recommendation,
            )

        # -----------------------------------------
        # 13. Return recommendations
        # -----------------------------------------

        return top_ranked
    def get_latest_recommendations(
        self,
        db,
        user_id: int,
        limit: int = 5,
    ):
        return (
            recommendation_repository
            .get_latest_for_user(
                db,
                user_id,
                limit,
            )
        )


recommendation_service = RecommendationService()