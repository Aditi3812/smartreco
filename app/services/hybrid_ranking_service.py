from typing import List


class HybridRankingService:
    """
    Combines behavioral and semantic signals
    into a single recommendation score.
    """

    BEHAVIOR_WEIGHT = 0.50
    SEMANTIC_WEIGHT = 0.35
    PREFERENCE_WEIGHT = 0.15

    def calculate_preference_score(
        self,
        product,
        behavior_profile,
    ) -> float:

        score = 0.0

        # -----------------------------
        # Category preference
        # -----------------------------

        category_scores = (
            behavior_profile.category_scores
            or {}
        )

        category_score = category_scores.get(
            product.category,
            0.0,
        )

        score += category_score * 0.6

        # -----------------------------
        # Difficulty preference
        # -----------------------------

        difficulty_scores = (
            behavior_profile.difficulty_scores
            or {}
        )

        difficulty_score = difficulty_scores.get(
            product.difficulty,
            0.0,
        )

        score += difficulty_score * 0.4

        return min(score, 1.0)

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

    def rank_candidates(
        self,
        candidates,
        behavior_profile,
    ):

        ranked = []

        for candidate in candidates:

            product = candidate["product"]

            behavioral_score = candidate.get(
                "behavioral_score",
                0.0,
            )

            semantic_score = candidate.get(
                "semantic_score",
                0.0,
            )

            preference_score = (
                self.calculate_preference_score(
                    product,
                    behavior_profile,
                )
            )

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

        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True,
        )

        return ranked


hybrid_ranking_service = HybridRankingService()