
from app.database.database import SessionLocal

from app.agents.recommendation_agent import (
    recommendation_agent,
)


db = SessionLocal()

try:

    result = recommendation_agent.invoke(
        {
            "user_id": 3,
            "limit": 5,
            "db": db,
        }
    )

    print("\n")
    print("=" * 80)
    print("SMARTRECO — HYBRID RANKING TEST")
    print("=" * 80)

    # =====================================================
    # CANDIDATES
    # =====================================================

    print("\n")
    print("CANDIDATES")
    print("-" * 80)

    for candidate in result.get(
        "candidates",
        [],
    ):

        product = candidate["product"]

        print(
            f"{product.id:<4}"
            f"{product.title:<35}"
            f"Semantic: "
            f"{candidate['semantic_score']:.4f}"
        )

    # =====================================================
    # RANKED RECOMMENDATIONS
    # =====================================================

    print("\n")
    print("HYBRID RANKED RECOMMENDATIONS")
    print("-" * 80)

    ranked = result.get(
        "ranked_recommendations",
        [],
    )

    for rank, item in enumerate(
        ranked,
        start=1,
    ):

        product = item["product"]

        print(
            f"{rank:<4}"
            f"{product.id:<4}"
            f"{product.title:<35}"
        )

        print(
            f"     Behavioral : "
            f"{item['behavioral_score']:.4f}"
        )

        print(
            f"     Semantic   : "
            f"{item['semantic_score']:.4f}"
        )

        print(
            f"     Preference : "
            f"{item['preference_score']:.4f}"
        )

        print(
            f"     FINAL      : "
            f"{item['final_score']:.4f}"
        )

        print()

    # =====================================================
    # FINAL TOP PRODUCTS
    # =====================================================

    print("=" * 80)
    print("FINAL TOP RECOMMENDATIONS")
    print("=" * 80)

    for rank, item in enumerate(
        ranked,
        start=1,
    ):

        product = item["product"]

        print(
            f"{rank}. "
            f"{product.title} "
            f"(score={item['final_score']:.4f})"
        )

    print("=" * 80)

finally:

    db.close()
