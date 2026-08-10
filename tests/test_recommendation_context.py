from app.database.database import SessionLocal

from app.services.recommendation_context_service import (
    recommendation_context_service,
)


db = SessionLocal()

try:

    user_id = 3

    context = (
        recommendation_context_service.build_context(
            db,
            user_id,
        )
    )

    print("\n")
    print("=" * 100)
    print("                 RECOMMENDATION CONTEXT")
    print("=" * 100)

    print(
        "\nUSER ID:",
        context["user_id"],
    )

    # --------------------------------
    # Behavior Profile
    # --------------------------------

    profile = (
        context["behavior_profile"]
    )

    print("\n===== BEHAVIOR PROFILE =====")

    if profile:

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
            "Purchase Intent:",
            profile.purchase_intent,
        )

    else:

        print("No behavior profile found.")

    # --------------------------------
    # Top Products
    # --------------------------------

    print("\n===== TOP PRODUCTS =====")

    for rank, interaction in enumerate(
        context["top_products"],
        start=1,
    ):

        print(
            rank,
            "| Product:",
            interaction.product_id,
            "| Score:",
            interaction.final_score,
        )

    # --------------------------------
    # Recent Events
    # --------------------------------

    print("\n===== RECENT EVENTS =====")

    for event in context["recent_events"]:

        print(
            event.id,
            "|",
            event.event_type,
            "| Product:",
            event.product_id,
            "|",
            event.created_at,
        )

    print("\n" + "=" * 100)

finally:

    db.close()