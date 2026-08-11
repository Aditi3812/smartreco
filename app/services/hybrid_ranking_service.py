import math
from datetime import datetime, timezone


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
    # INTERNAL: On-the-fly interaction score
    # =========================================================

    def _compute_interaction_score_from_raw(
        self,
        interaction,
    ) -> float:
        """
        Replicates ProductInteractionService.calculate_interaction_score()
        on-the-fly using the raw metric columns that are always populated
        by the Phase-2 event pipeline, even when the pre-computed
        interaction_score / final_score columns are None or zero.
        """

        MAX_VIEWS = 20
        MAX_TIME = 300
        MAX_SEARCHES = 5

        view_count = interaction.view_count or 0
        total_time_spent = interaction.total_time_spent or 0.0
        max_scroll_depth = interaction.max_scroll_depth or 0.0
        search_count = interaction.search_count or 0

        view_score = (
            math.log1p(view_count)
            / math.log1p(MAX_VIEWS)
        )
        view_score = min(view_score, 1.0)

        time_score = min(total_time_spent / MAX_TIME, 1.0)

        scroll_score = min(max_scroll_depth / 100, 1.0)

        search_score = min(search_count / MAX_SEARCHES, 1.0)

        score = (
            0.30 * view_score
            + 0.30 * time_score
            + 0.25 * scroll_score
            + 0.15 * search_score
        )

        return round(score, 4)

    # =========================================================
    # INTERNAL: On-the-fly recency score
    # =========================================================

    def _compute_recency_score_from_raw(
        self,
        interaction,
    ) -> float:
        """
        Replicates ProductInteractionService.calculate_recency_score()
        using the last_interacted_at column that is always written by
        the Phase-2 event pipeline.
        """

        if not interaction.last_interacted_at:
            return 1.0

        now = datetime.now(timezone.utc)
        last_at = interaction.last_interacted_at

        if last_at.tzinfo is None:
            last_at = last_at.replace(tzinfo=timezone.utc)

        age_days = (now - last_at).total_seconds() / 86400

        return round(math.exp(-0.1 * age_days), 4)

    # =========================================================
    # 1. BEHAVIORAL SCORE
    # =========================================================

    def calculate_behavioral_score(
        self,
        product_id: int,
        interactions,
        behavior_profile=None,
        product=None,
    ) -> float:
        """
        Returns a behavioral score for a candidate product using a
        three-tier resolution strategy:

        Tier 1 — Direct interaction with a valid pre-computed final_score.
            Use it directly; it already encodes interaction + recency.

        Tier 2 — Direct interaction exists but final_score is None or 0.0.
            Compute the score on-the-fly from the raw metric columns
            (view_count, total_time_spent, max_scroll_depth, search_count)
            that the Phase-2 event pipeline always populates, then apply
            the same recency decay used by ProductInteractionService.

        Tier 3 — No direct interaction record for this candidate product.
            Common for vector-retrieved items the user has never viewed.
            Use 50 % of the user's category engagement score from
            behavior_profile as a proportional cold-start fallback
            instead of hard-coding 0.0.
        """

        # ----------------------------------------------------------
        # Tier 1 & Tier 2: scan existing interaction records
        # ----------------------------------------------------------

        for interaction in interactions:

            if interaction.product_id != product_id:
                continue

            # ---- Tier 1: valid pre-computed final_score ----

            final_score = interaction.final_score

            if final_score is not None and float(final_score) > 0.0:
                return max(0.0, min(float(final_score), 1.0))

            # ---- Tier 2: on-the-fly computation from raw metrics ----

            interaction_score = self._compute_interaction_score_from_raw(
                interaction
            )
            recency_score = self._compute_recency_score_from_raw(
                interaction
            )

            computed = round(interaction_score * recency_score, 4)
            return max(0.0, min(computed, 1.0))

        # ----------------------------------------------------------
        # Tier 3: no direct interaction — category engagement fallback
        # ----------------------------------------------------------

        if behavior_profile is not None and product is not None:

            category_scores = (
                behavior_profile.category_scores
                or {}
            )

            cat_score = category_scores.get(
                product.category,
                0.0,
            )

            # 50 % of category engagement is a proportional
            # signal that avoids collapsing cold-start candidates
            # to a uniform zero while remaining clearly below
            # genuinely interacted-with products.
            fallback = round(0.5 * float(cat_score), 4)
            return max(0.0, min(fallback, 1.0))

        return 0.0

    # =========================================================
    # 2. PREFERENCE SCORE
    # =========================================================

    def calculate_preference_score(
        self,
        product,
        behavior_profile,
    ) -> float:

        if behavior_profile is None:
            return 0.0

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
        interactions=None,
    ):
        """
        Ranks all candidates by hybrid score.

        `interactions` defaults to [] so that the two-argument call
        from recommendation_service.py degrades gracefully to the
        Tier 3 category fallback instead of raising a TypeError.
        """

        if interactions is None:
            interactions = []

        ranked = []

        for candidate in candidates:

            product = candidate["product"]

            product_id = product.id

            # -----------------------------------------
            # Behavioral signal (three-tier)
            # -----------------------------------------

            behavioral_score = (
                self.calculate_behavioral_score(
                    product_id,
                    interactions,
                    behavior_profile=behavior_profile,
                    product=product,
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
