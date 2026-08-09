from app.services.qdrant_service import qdrant_service
from app.services.user_embedding_service import (
    user_embedding_service,
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

        # -----------------------------------------
        # Generate user preference embedding
        # -----------------------------------------

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

        # -----------------------------------------
        # Search Qdrant
        # -----------------------------------------

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
        }


semantic_retrieval_service = (
    SemanticRetrievalService()
)