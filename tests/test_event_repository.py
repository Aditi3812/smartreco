from app.database.database import SessionLocal
from app.repositories.event_repository import event_repository
from app.schemas.event import EventCreate


db = SessionLocal()


event = event_repository.create_event(
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