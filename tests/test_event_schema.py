from app.schemas.event import EventCreate


event = EventCreate(
    event_type="PRODUCT_VIEW",
    product_id=1,
    category="AI",
)

print(event)