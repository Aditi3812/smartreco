from app.database.database import SessionLocal
from app.models.event import Event
from app.models.product_interaction import ProductInteraction
from datetime import datetime, timezone

db = SessionLocal()
try:
    user_id = 4
    events = db.query(Event).filter(Event.user_id == user_id).all()
    print("=" * 60)
    print(f"RAW EVENT INSPECTION FOR USER {user_id}")
    print("=" * 60)
    print(f"Total raw events found: {len(events)}")

    # Load all existing database interactions for this user into a memory map
    existing_records = {
        i.product_id: i 
        for i in db.query(ProductInteraction).filter_by(user_id=user_id).all()
    }

    updated_count = 0
    created_count = 0

    for e in events:
        # Resolve product_id from column or event_metadata dict
        p_id = getattr(e, 'product_id', None)
        if not p_id and isinstance(e.event_metadata, dict):
            p_id = e.event_metadata.get('product_id')

        if p_id:
            p_id = int(p_id)
            if p_id in existing_records:
                # Update in-memory record
                record = existing_records[p_id]
                record.view_count += 1
                if e.created_at and (not record.last_interacted_at or e.created_at > record.last_interacted_at):
                    record.last_interacted_at = e.created_at
                updated_count += 1
            else:
                # Create new record and track in memory map to avoid duplicates
                new_record = ProductInteraction(
                    user_id=user_id,
                    product_id=p_id,
                    view_count=1,
                    last_interacted_at=e.created_at or datetime.now(timezone.utc)
                )
                db.add(new_record)
                existing_records[p_id] = new_record
                created_count += 1

    db.commit()
    print("-" * 60)
    print(f"SUCCESS: Created {created_count} new interaction records | Updated {updated_count} existing records.")
    print("-" * 60)

except Exception as err:
    db.rollback()
    print(f"\nError occurred: {err}")
finally:
    db.close()