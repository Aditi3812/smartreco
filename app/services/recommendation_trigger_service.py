from datetime import datetime, UTC, timedelta

from app.repositories.recommendation_repository import (
    recommendation_repository,
)
from app.repositories.product_interaction_repository import (
    product_interaction_repository,
)


class RecommendationTriggerService:
    """
    Determines whether a user's recommendations
    should be regenerated.
    """

    RECOMMENDATION_TTL_HOURS = 24
    NEW_INTERACTION_THRESHOLD = 5

    def should_generate(
        self,
        db,
        user_id: int,
    ) -> bool:

        # -----------------------------------------
        # 1. Check previous recommendations
        # -----------------------------------------

        latest = (
            recommendation_repository
            .get_latest_for_user(
                db,
                user_id,
                limit=1,
            )
        )

        # No recommendations exist yet
        if not latest:
            return True

        # -----------------------------------------
        # 2. Check recommendation freshness
        # -----------------------------------------

        latest_created_at = latest[0].created_at

        now = datetime.now(UTC)

        if (
            now - latest_created_at
            > timedelta(
                hours=self.RECOMMENDATION_TTL_HOURS
            )
        ):
            return True

        # -----------------------------------------
        # 3. Check NEW interactions
        # -----------------------------------------

        interactions = (
            product_interaction_repository
            .get_by_user(
                db,
                user_id,
            )
        )

        new_interactions = [
            interaction
            for interaction in interactions
            if interaction.last_interacted_at
            > latest_created_at
        ]

        if len(new_interactions) >= self.NEW_INTERACTION_THRESHOLD:
            return True
        # -----------------------------------------
        # Nothing triggered
        # -----------------------------------------

        return False


recommendation_trigger_service = (
    RecommendationTriggerService()
)