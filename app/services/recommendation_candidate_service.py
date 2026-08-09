from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_interaction_repository import (
    product_interaction_repository,
)


class RecommendationCandidateService:
    """
    Generates and behaviorally ranks
    recommendation candidates.
    """

    def generate_candidates(
        self,
        db: Session,
        context: dict,
        limit: int = 20,
    ):

        profile = context.get(
            "behavior_profile"
        )
        user_id = context.get("user_id")
        print("\n===== CANDIDATE DEBUG =====")
        print("User ID:", user_id)

        if user_id:
            interactions = (
                product_interaction_repository.get_by_user(
                    db,
                    user_id,
                )
            )

            print(
                "Interacted product IDs:",
                [i.product_id for i in interactions],
            )

            print(
                "Interaction count:",
                len(interactions),
            )

        # --------------------------------
        # Get all products
        # --------------------------------

        products = (
            db.query(Product)
            .all()
        )

        # --------------------------------
        # Cold-start fallback
        # --------------------------------

        if not profile:

            return products[:limit]

        category_scores = (
            profile.category_scores
            or {}
        )

        difficulty_scores = (
            profile.difficulty_scores
            or {}
        )

        language_scores = (
            profile.language_scores
            or {}
        )

        # --------------------------------
        # Get user's product interactions
        # --------------------------------

        interacted_product_ids = set()

        if user_id:

            interactions = (
                product_interaction_repository.get_by_user(
                    db,
                    user_id,
                )
            )

            for interaction in interactions:

                interacted_product_ids.add(
                    interaction.product_id
                )

        # --------------------------------
        # Score products
        # --------------------------------

        scored_products = []

        for product in products:

            # --------------------------------
            # Skip already interacted products
            # --------------------------------

            if (
                product.id
                in interacted_product_ids
            ):
                continue

            # --------------------------------
            # Category score
            # --------------------------------

            category_score = (
                category_scores.get(
                    product.category,
                    0,
                )
            )

            # --------------------------------
            # Difficulty score
            # --------------------------------

            difficulty_score = (
                difficulty_scores.get(
                    product.difficulty,
                    0,
                )
            )

            # --------------------------------
            # Language score
            # --------------------------------

            language_score = (
                language_scores.get(
                    product.language,
                    0,
                )
            )

            # --------------------------------
            # Final behavioral score
            # --------------------------------

            score = (
                0.50 * category_score
                + 0.30 * difficulty_score
                + 0.20 * language_score
            )

            scored_products.append(
                (
                    product,
                    score,
                )
            )

        # --------------------------------
        # Sort highest → lowest
        # --------------------------------

        scored_products.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        # --------------------------------
        # Return top candidates
        # --------------------------------

        return [
            product
            for product, score
            in scored_products[:limit]
        ]


recommendation_candidate_service = (
    RecommendationCandidateService()
)