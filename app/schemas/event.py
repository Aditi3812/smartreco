from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):

    event_type: str

    session_id: str | None = None

    product_id: int | None = None

    category: str | None = None

    search_query: str | None = None

    event_metadata: str | None = None


class EventResponse(BaseModel):

    id: int

    user_id: int | None

    event_type: str

    session_id: str | None

    product_id: int | None

    category: str | None

    search_query: str | None

    event_metadata: str | None

    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )