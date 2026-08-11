from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate


class EventRepository:
    """
    Handles database operations
    for behavioral events.
    """

    def create_event(
        self,
        db: Session,
        event_data: EventCreate,
        user_id: int | None = None,
    ):

        event = Event(
            user_id=user_id,
            event_type=event_data.event_type,
            session_id=event_data.session_id,
            product_id=event_data.product_id,
            category=event_data.category,
            search_query=event_data.search_query,
            event_metadata=event_data.event_metadata,
        )

        db.add(event)
        db.flush()
        db.refresh(event)

        return event


    def get_user_events(
        self,
        db: Session,
        user_id: int,
    ):

        return (
            db.query(Event)
            .filter(
                Event.user_id == user_id
            )
            .order_by(
                Event.created_at.desc()
            )
            .all()
        )


    def get_recent_events(
        self,
        db: Session,
        limit: int = 50,
    ):

        return (
            db.query(Event)
            .order_by(
                Event.created_at.desc()
            )
            .limit(limit)
            .all()
        )
    def get_by_user_id(
    self,
    db: Session,
    user_id: int,
):
        return (
            db.query(Event)
            .filter(
                Event.user_id == user_id
            )
            .all()
        )
    def get_recent_by_user(
        self,
        db: Session,
        user_id: int,
        limit: int = 10,
    ):

        return (
            db.query(Event)
            .filter(
                Event.user_id == user_id
            )
            .order_by(
                Event.created_at.desc()
            )
            .limit(limit)
            .all()
        )
event_repository = EventRepository()