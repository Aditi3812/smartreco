
class HybridRankingService:
    """
    Combines three independent recommendation signals:

    1. Behavioral signal
       -> How strongly the user has interacted with a product.

    2. Semantic signal
       -> How semantically relevant the product is to the user's
          current interests.

    3. Preference signal
       -> How well the product matches the user's learned
          category and difficulty preferences.
    """

    BEHAVIOR_WEIGHT = 0.50
    SEMANTIC_WEIGHT = 0.35
    PREFERENCE_WEIGHT = 0.15

    # =========================================================
    # 1. BEHAVIORAL SCORE
    # =========================================================

    def calculate_behavioral_score(
        self,
        product_id: int,
        interactions,
    ) -> float:
        """
        Returns the existing product-level behavioral score.

        ProductInteraction already stores:
            interaction_score
            recency_score
            final_score

        We use final_score because it represents the combined
        behavioral + recency signal for that user/product pair.

        If the product has never been interacted with,
        behavioral_score = 0.0.
        """

        for interaction in interactions:

            if interaction.product_id == product_id:

                score = interaction.final_score

                if score is None:
                    return 0.0

                return max(
                    0.0,
                    min(float(score), 1.0),
                )

        return 0.0

    # =========================================================
    # 2. PREFERENCE SCORE
    # =========================================================

    def calculate_preference_score(
        self,
        product,
        behavior_profile,
    ) -> float:

        score = 0.0

        # -----------------------------------------
        # Category preference
        # -----------------------------------------

        category_scores = (
            behavior_profile.category_scores
            or {}
        )

        category_score = category_scores.get(
            product.category,
            0.0,
        )

        score += category_score * 0.6

        # -----------------------------------------
        # Difficulty preference
        # -----------------------------------------

        difficulty_scores = (
            behavior_profile.difficulty_scores
            or {}
        )

        difficulty_score = difficulty_scores.get(
            product.difficulty,
            0.0,
        )

        score += difficulty_score * 0.4

        return max(
            0.0,
            min(score, 1.0),
        )

    # =========================================================
    # 3. HYBRID SCORE
    # =========================================================

    def calculate_hybrid_score(
        self,
        behavioral_score: float,
        semantic_score: float,
        preference_score: float,
    ) -> float:

        final_score = (
            self.BEHAVIOR_WEIGHT
            * behavioral_score
            +
            self.SEMANTIC_WEIGHT
            * semantic_score
            +
            self.PREFERENCE_WEIGHT
            * preference_score
        )

        return round(
            final_score,
            4,
        )

    # =========================================================
    # 4. RANK CANDIDATES
    # =========================================================

    def rank_candidates(
        self,
        candidates,
        behavior_profile,
        interactions,
    ):

        ranked = []

        for candidate in candidates:

            product = candidate["product"]

            product_id = product.id

            # -----------------------------------------
            # Behavioral signal
            # -----------------------------------------

            behavioral_score = (
                self.calculate_behavioral_score(
                    product_id,
                    interactions,
                )
            )

            # -----------------------------------------
            # Semantic signal
            # -----------------------------------------

            semantic_score = float(
                candidate.get(
                    "semantic_score",
                    0.0,
                )
            )

            # -----------------------------------------
            # Preference signal
            # -----------------------------------------

            preference_score = (
                self.calculate_preference_score(
                    product,
                    behavior_profile,
                )
            )

            # -----------------------------------------
            # Final hybrid score
            # -----------------------------------------

            final_score = (
                self.calculate_hybrid_score(
                    behavioral_score,
                    semantic_score,
                    preference_score,
                )
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

        # -----------------------------------------
        # Highest score first
        # -----------------------------------------

        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True,
        )

        return ranked


hybrid_ranking_service = HybridRankingService()
