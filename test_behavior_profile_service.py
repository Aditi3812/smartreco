from app.database.database import SessionLocal

from app.services.behavior_profile_service import (
    behavior_profile_service,
)


db = SessionLocal()

try:

    user_id = 3  # CHANGE THIS to an actual user ID

    profile = (
        behavior_profile_service.build_profile(
            db,
            user_id,
        )
    )

    print("\n===== BEHAVIOR PROFILE =====")

    print(
        "User ID:",
        profile.user_id,
    )

    print(
        "Category Scores:",
        profile.category_scores,
    )

    print(
        "Difficulty Scores:",
        profile.difficulty_scores,
    )

    print(
        "Language Scores:",
        profile.language_scores,
    )

    print(
        "Search Frequency:",
        profile.search_frequency,
    )

    print(
        "Average Time:",
        profile.average_time_spent,
    )

    print(
        "Average Scroll:",
        profile.average_scroll_depth,
    )
    print(
        "Purchase Intent:",
        profile.purchase_intent,
    )
    print(
        "Total Events:",
        profile.total_events,
    )

finally:

    db.close()