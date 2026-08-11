
from app.services.qdrant_service import (
    qdrant_service,
)

from app.services.user_embedding_service import (
    user_embedding_service,
)

from app.repositories.product_repository import (
    product_repository,
)


class SemanticRetrievalService:

    def retrieve_for_user(
        self,
        db,
        user_id: int,
        behavior_profile,
        top_products,
        limit: int = 5,
    ):

        # =====================================================
        # 1. PERSONALIZED RETRIEVAL
        # =====================================================

        if behavior_profile:

            (
                preference_text,
                user_embedding,
            ) = (
                user_embedding_service
                .generate_user_embedding(
                    behavior_profile,
                    top_products,
                )
            )

            # ---------------------------------------------
            # Search Qdrant using user embedding
            # ---------------------------------------------

            results = (
                qdrant_service
                .search_products(
                    user_embedding,
                    limit=limit,
                )
            )

            return {
                "preference_text": preference_text,
                "results": results,
                "cold_start": False,
            }

        # =====================================================
        # 2. COLD-START RETRIEVAL
        # =====================================================

        # User has no behavior profile yet.
        #
        # We cannot generate a personalized embedding,
        # so return a small product catalogue as the
        # initial recommendation pool.

        products = (
            product_repository
            .get_all_products(
                db,
                skip=0,
                limit=limit,
            )
        )

        # -----------------------------------------------------
        # Create lightweight retrieval results
        # -----------------------------------------------------
        #
        # The hybrid ranking service expects candidates
        # to eventually contain a semantic score.
        #
        # Since there is no semantic similarity for a
        # cold-start user, use a neutral baseline score.

        results = []

        for product in products:

            results.append(
                {
                    "product": product,
                    "semantic_score": 0.0,
                }
            )

        return {
            "preference_text": (
                "No behavioral profile available. "
                "Using cold-start product recommendations."
            ),
            "results": results,
            "cold_start": True,
        }


semantic_retrieval_service = (
    SemanticRetrievalService()
)
