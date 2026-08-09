from sqlalchemy.orm import Session

from app.repositories.behavior_profile_repository import (
    behavior_profile_repository,
)

from app.repositories.product_interaction_repository import (
    product_interaction_repository,
)

from app.repositories.event_repository import (
    event_repository,
)


class RecommendationContextService:
    """
    Builds a compact behavioral context
    for the recommendation engine.
    """

    def __init__(self):

        self.behavior_profile_repository = (
            behavior_profile_repository
        )

        self.product_interaction_repository = (
            product_interaction_repository
        )

        self.event_repository = (
            event_repository
        )

    def build_context(
        self,
        db: Session,
        user_id: int,
        top_products_limit: int = 5,
        recent_events_limit: int = 10,
    ):

        # --------------------------------
        # Behavior Profile
        # --------------------------------

        behavior_profile = (
            self.behavior_profile_repository.get_by_user_id(
                db,
                user_id,
            )
        )

        # --------------------------------
        # Top Products
        # --------------------------------

        top_products = (
            self.product_interaction_repository.get_top_by_user(
                db,
                user_id,
                top_products_limit,
            )
        )

        # --------------------------------
        # Recent Events
        # --------------------------------

        recent_events = (
            self.event_repository.get_recent_by_user(
                db,
                user_id,
                recent_events_limit,
            )
        )

        return {
            "user_id": user_id,

            "behavior_profile": (
                behavior_profile
            ),

            "top_products": top_products,

            "recent_events": recent_events,
        }


recommendation_context_service = (
    RecommendationContextService()
)