from sqlalchemy.orm import Session

from app.repositories.event_repository import event_repository
from app.schemas.event import EventCreate


class EventService:
    """
    Handles behavioral event business logic.
    """

    ALLOWED_EVENTS = {
        "PAGE_VIEW",
        "SEARCH",
        "PRODUCT_VIEW",
        "PRODUCT_CLICK",
        "CATEGORY_VIEW",
        "SCROLL_DEPTH",
        "TIME_SPENT",
        "ADD_TO_CART",
        "BOOKMARK",
        "PURCHASE",
        "FILTER"
    }


    def __init__(self):
        self.event_repository = event_repository


    def create_event(
        self,
        db: Session,
        event_data: EventCreate,
        user_id: int | None = None,
    ):

        # Validate event type

        if event_data.event_type not in self.ALLOWED_EVENTS:
            raise ValueError(
                "Invalid event type."
            )


        # Additional validation

        if (
            event_data.event_type == "PRODUCT_VIEW"
            and not event_data.product_id
        ):
            raise ValueError(
                "Product view requires product_id."
            )


        if (
            event_data.event_type == "SEARCH"
            and not event_data.search_query
        ):
            raise ValueError(
                "Search event requires search_query."
            )


        return self.event_repository.create_event(
            db,
            event_data,
            user_id,
        )


    def get_user_events(
        self,
        db: Session,
        user_id: int,
    ):

        return self.event_repository.get_user_events(
            db,
            user_id,
        )


    def get_recent_events(
        self,
        db: Session,
        limit: int = 50,
    ):

        return self.event_repository.get_recent_events(
            db,
            limit,
        )


event_service = EventService()