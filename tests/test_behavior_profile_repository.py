from app.database.database import SessionLocal
from app.repositories.behavior_profile_repository import (
    behavior_profile_repository,
)


db = SessionLocal()

try:

    profile = (
        behavior_profile_repository.get_or_create(
            db,
            3,
        )
    )

    print("Profile ID:", profile.id)
    print("User ID:", profile.user_id)
    print("Category scores:", profile.category_scores)
    print(
        "Search frequency:",
        profile.search_frequency,
    )

finally:

    db.close()