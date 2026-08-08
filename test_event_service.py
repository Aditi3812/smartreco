from app.database.database import SessionLocal

from app.schemas.event import EventCreate
from app.services.event_service import event_service


db = SessionLocal()


event = event_service.create_event(
    db,
    EventCreate(
        event_type="PRODUCT_VIEW",
        product_id=1,
        category="AI",
    ),
    user_id=3,
)


print(event.id)
print(event.event_type)


db.close()