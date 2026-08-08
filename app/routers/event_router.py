from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.event import (
    EventCreate,
    EventResponse,
)
from app.services.event_service import event_service
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "",
    response_model=EventResponse,
)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    try:

        return event_service.create_event(
            db,
            event,
            user_id=current_user.id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )



@router.get(
    "/me",
    response_model=list[EventResponse],
)
def get_my_events(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return event_service.get_user_events(
        db,
        current_user.id,
    )