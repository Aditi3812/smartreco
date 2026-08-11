from app.database.database import SessionLocal
from app.models.event import Event
from app.models.product_interaction import ProductInteraction
from datetime import datetime, timezone

def backfill_product_interactions():
    db = SessionLocal()
    try:
        events = db.query(Event).all()
        print(f"Processing {len(events)} events...")
        
        interactions_map = {}

        for e in events:
            user_id = e.user_id
            meta = e.event_metadata or {}
            product_id = meta.get("product_id") if isinstance(meta, dict) else None
            
            if not user_id or not product_id:
                continue

            key = (user_id, product_id)
            if key not in interactions_map:
                interactions_map[key] = {
                    "view_count": 0,
                    "search_count": 0,
                    "total_time_spent": 0.0,
                    "max_scroll_depth": 0.0,
                    "last_interacted_at": e.created_at or datetime.now(timezone.utc)
                }

            stats = interactions_map[key]
            if e.event_type == "PRODUCT_VIEW":
                stats["view_count"] += 1
            elif e.event_type == "SEARCH":
                stats["search_count"] += 1

            if isinstance(meta, dict):
                stats["total_time_spent"] += float(meta.get("time_spent", 0.0))
                stats["max_scroll_depth"] = max(stats["max_scroll_depth"], float(meta.get("scroll_depth", 0.0)))

        # Upsert into PostgreSQL
        for (u_id, p_id), stats in interactions_map.items():
            existing = db.query(ProductInteraction).filter_by(user_id=u_id, product_id=p_id).first()
            if not existing:
                existing = ProductInteraction(user_id=u_id, product_id=p_id)
                db.add(existing)

            existing.view_count = stats["view_count"]
            existing.search_count = stats["search_count"]
            existing.total_time_spent = stats["total_time_spent"]
            existing.max_scroll_depth = stats["max_scroll_depth"]
            existing.last_interacted_at = stats["last_interacted_at"]

        db.commit()
        print("Backfill complete!")

    finally:
        db.close()

if __name__ == "__main__":
    backfill_product_interactions()