from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def build_product_text(self, product):

        parts = [
            product.title,
            product.description,
            f"Category: {product.category}",
            f"Difficulty: {product.difficulty}",
            f"Language: {product.language}",
            f"Skills: {product.skills}",
            f"Tags: {product.tags}",
        ]

        return "\n".join(
            str(part)
            for part in parts
            if part
        )

    def generate_product_embedding(
        self,
        product,
    ):

        text = self.build_product_text(
            product
        )

        embedding = self.model.encode(
            text
        )

        return embedding.tolist()

    def build_user_interest_text(
        self,
        behavior_profile,
        top_products,
        recent_events,
    ):

        parts = []

        # -----------------------------
        # Category interests
        # -----------------------------

        if behavior_profile:

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

            # -----------------------------
            # Difficulty interests
            # -----------------------------

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

            # -----------------------------
            # Language interests
            # -----------------------------

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

        # -----------------------------
        # Previously interacted products
        # -----------------------------

        if top_products:

            for interaction in top_products[:5]:

                if interaction.product:

                    product = interaction.product

                    parts.append(
                        f"Previously interested in: "
                        f"{product.title}. "
                        f"{product.description}. "
                        f"Skills: {product.skills}. "
                        f"Tags: {product.tags}."
                    )

        # -----------------------------
        # Recent searches
        # -----------------------------

        if recent_events:

            searches = []

            for event in recent_events:

                if (
                    event.event_type == "SEARCH"
                    and event.search_query
                ):
                    searches.append(
                        event.search_query
                    )

            if searches:

                parts.append(
                    "Recent searches: "
                    + ", ".join(searches[:5])
                )

        return "\n".join(parts)

    def generate_user_embedding(
        self,
        user_interest_text,
    ):

        embedding = self.model.encode(
            user_interest_text
        )

        return embedding.tolist()


embedding_service = EmbeddingService()