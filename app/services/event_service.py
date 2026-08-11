from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.repositories.event_repository import event_repository
from app.schemas.event import EventCreate
from app.models.product_interaction import ProductInteraction
from app.services.behavior_profile_service import behavior_profile_service

class EventService:
    """
    Handles behavioral event business logic and maintains downstream
    aggregations for product interactions and behavior profiles.
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
        # 1. Validate event type
        if event_data.event_type not in self.ALLOWED_EVENTS:
            raise ValueError("Invalid event type.")

        if (
            event_data.event_type == "PRODUCT_VIEW"
            and not event_data.product_id
        ):
            raise ValueError("Product view requires product_id.")

        if (
            event_data.event_type == "SEARCH"
            and not event_data.search_query
        ):
            raise ValueError("Search event requires search_query.")

        # 2. Save raw event via event repository
        event = self.event_repository.create_event(
            db,
            event_data,
            user_id,
        )

        # 3. Process product interactions if user and product exist
        if user_id and event_data.product_id:
            self._update_product_interaction(db, user_id, event_data)

        # 4. Automatically update user behavior profile
        if user_id:
            try:
                behavior_profile_service.build_profile(db, user_id)
            except Exception as e:
                print(f"[EventService] Profile update warning for user {user_id}: {e}")

        db.commit()
        db.refresh(event)

        return event

    def _update_product_interaction(
        self,
        db: Session,
        user_id: int,
        event_data: EventCreate,
    ):
        import json as _json
        raw_meta = event_data.event_metadata
        if isinstance(raw_meta, str):
            try:
                metadata = _json.loads(raw_meta)
            except _json.JSONDecodeError:
                metadata = {}
        elif isinstance(raw_meta, dict):
            metadata = raw_meta
        else:
            metadata = {}
        time_spent = float(metadata.get("time_spent", 0.0))
        scroll_depth = float(metadata.get("scroll_depth", 0.0))

        interaction = (
            db.query(ProductInteraction)
            .filter_by(user_id=user_id, product_id=event_data.product_id)
            .first()
        )

        if not interaction:
            interaction = ProductInteraction(
                user_id=user_id,
                product_id=event_data.product_id,
                view_count=1 if event_data.event_type in ["PRODUCT_VIEW", "PRODUCT_CLICK"] else 0,
                search_count=1 if event_data.event_type == "SEARCH" else 0,
                total_time_spent=time_spent,
                max_scroll_depth=scroll_depth,
                last_interacted_at=datetime.now(timezone.utc),
            )
            db.add(interaction)
        else:
            if event_data.event_type in ["PRODUCT_VIEW", "PRODUCT_CLICK"]:
                interaction.view_count = (interaction.view_count or 0) + 1
            elif event_data.event_type == "SEARCH":
                interaction.search_count = (interaction.search_count or 0) + 1

            if time_spent > 0:
                interaction.total_time_spent = (interaction.total_time_spent or 0.0) + time_spent

            if scroll_depth > (interaction.max_scroll_depth or 0.0):
                interaction.max_scroll_depth = scroll_depth

            interaction.last_interacted_at = datetime.now(timezone.utc)

        db.flush()

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