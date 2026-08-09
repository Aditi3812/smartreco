from app.services.embedding_service import (
    embedding_service,
)


class UserEmbeddingService:

    def build_user_preference_text(
        self,
        behavior_profile,
        top_products,
    ):

        parts = []

        # -----------------------------------------
        # Category preferences
        # -----------------------------------------

        category_scores = (
            behavior_profile.category_scores
            or {}
        )

        if category_scores:

            categories = sorted(
                category_scores.items(),
                key=lambda x: x[1],
                reverse=True,
            )

            category_text = ", ".join(
                category
                for category, score
                in categories[:5]
            )

            parts.append(
                f"Interested categories: "
                f"{category_text}"
            )

        # -----------------------------------------
        # Difficulty preferences
        # -----------------------------------------

        difficulty_scores = (
            behavior_profile.difficulty_scores
            or {}
        )

        if difficulty_scores:

            difficulties = sorted(
                difficulty_scores.items(),
                key=lambda x: x[1],
                reverse=True,
            )

            difficulty_text = ", ".join(
                difficulty
                for difficulty, score
                in difficulties[:3]
            )

            parts.append(
                f"Preferred difficulty levels: "
                f"{difficulty_text}"
            )

        # -----------------------------------------
        # Language preferences
        # -----------------------------------------

        language_scores = (
            behavior_profile.language_scores
            or {}
        )

        if language_scores:

            languages = sorted(
                language_scores.items(),
                key=lambda x: x[1],
                reverse=True,
            )

            language_text = ", ".join(
                language
                for language, score
                in languages[:3]
            )

            parts.append(
                f"Preferred languages: "
                f"{language_text}"
            )

        # -----------------------------------------
        # Behavioral signals
        # -----------------------------------------

        parts.append(
            f"Search frequency: "
            f"{behavior_profile.search_frequency}"
        )

        parts.append(
            f"Average time spent: "
            f"{behavior_profile.average_time_spent}"
            f" seconds"
        )

        parts.append(
            f"Average scroll depth: "
            f"{behavior_profile.average_scroll_depth}%"
        )

        parts.append(
            f"Purchase intent: "
            f"{behavior_profile.purchase_intent}"
        )

        # -----------------------------------------
        # Previously interacted products
        # -----------------------------------------

        if top_products:

            product_names = []

            for interaction in top_products:

                if interaction.product:

                    product_names.append(
                        interaction.product.title
                    )

            if product_names:

                parts.append(
                    "Previously explored products: "
                    + ", ".join(product_names)
                )

        return "\n".join(parts)

    # -----------------------------------------
    # Generate user embedding
    # -----------------------------------------

    def generate_user_embedding(
        self,
        behavior_profile,
        top_products,
    ):

        text = (
            self.build_user_preference_text(
                behavior_profile,
                top_products,
            )
        )

        embedding = (
            embedding_service.model.encode(
                text
            )
        )

        return (
            text,
            embedding.tolist()
        )


user_embedding_service = (
    UserEmbeddingService()
)