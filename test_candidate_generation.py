from app.database.database import SessionLocal

from app.services.recommendation_context_service import (
    recommendation_context_service,
)

from app.services.recommendation_candidate_service import (
    recommendation_candidate_service,
)


db = SessionLocal()

try:

    user_id = 3

    # --------------------------------
    # Build context
    # --------------------------------

    context = (
        recommendation_context_service.build_context(
            db,
            user_id,
        )
    )

    profile = context[
        "behavior_profile"
    ]

    # --------------------------------
    # Generate candidates
    # --------------------------------

    candidates = (
        recommendation_candidate_service.generate_candidates(
            db,
            context,
            limit=20,
        )
    )

    print("\n")
    print("=" * 110)
    print("                 BEHAVIORALLY RANKED CANDIDATES")
    print("=" * 110)

    print(
        f"{'RANK':<7}"
        f"{'ID':<6}"
        f"{'PRODUCT':<32}"
        f"{'CATEGORY':<18}"
        f"{'DIFFICULTY':<15}"
        f"{'LANGUAGE':<12}"
    )

    print("-" * 110)

    for rank, product in enumerate(
        candidates,
        start=1,
    ):

        print(
            f"{rank:<7}"
            f"{product.id:<6}"
            f"{product.title[:30]:<32}"
            f"{product.category:<18}"
            f"{product.difficulty:<15}"
            f"{product.language:<12}"
        )

    print("=" * 110)

    print(
        "Total candidates:",
        len(candidates),
    )

finally:

    db.close()