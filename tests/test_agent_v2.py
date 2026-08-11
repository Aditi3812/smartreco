
from app.database.database import SessionLocal

from app.agents.recommendation_agent_v2 import (
    recommendation_agent_v2,
)


db = SessionLocal()

try:

    result = recommendation_agent_v2.invoke(
        {
            "user_id": 3,
            "limit": 5,
        }
    )
    
    print("\n")
    print("=" * 80)
    print("SMARTRECO — RECOMMENDATION AGENT V2 TEST")
    print("=" * 80)

    # =====================================================
    # TRIGGER
    # =====================================================

    print("\n")
    print("RECOMMENDATION TRIGGER")
    print("-" * 80)

    should_generate = result.get(
        "should_generate",
        None,
    )

    print(
        f"Should generate new recommendation: "
        f"{should_generate}"
    )

    if should_generate is True:

        print(
            "\n→ Trigger activated."
        )

        print(
            "→ Running behavior analysis, "
            "semantic retrieval, hybrid ranking "
            "and LLM generation."
        )

    elif should_generate is False:

        print(
            "\n→ Existing recommendation is still valid."
        )

        print(
            "→ Reusing previous recommendation."
        )

    else:

        print(
            "\n→ Trigger state was not returned."
        )

    # =====================================================
    # CANDIDATES
    # =====================================================

    candidates = result.get(
        "candidates",
        [],
    )

    if candidates:

        print("\n")
        print("CANDIDATES")
        print("-" * 80)

        for candidate in candidates:

            product = candidate["product"]

            print(
                f"{product.id:<4}"
                f"{product.title:<35}"
                f"Semantic: "
                f"{candidate.get('semantic_score', 0.0):.4f}"
            )

    # =====================================================
    # HYBRID RANKING
    # =====================================================

    ranked = result.get(
        "ranked_recommendations",
        [],
    )

    if ranked:

        print("\n")
        print("HYBRID RANKED RECOMMENDATIONS")
        print("-" * 80)

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
                f"{item.get('behavioral_score', 0.0):.4f}"
            )

            print(
                f"     Semantic   : "
                f"{item.get('semantic_score', 0.0):.4f}"
            )

            print(
                f"     Preference : "
                f"{item.get('preference_score', 0.0):.4f}"
            )

            print(
                f"     FINAL      : "
                f"{item.get('final_score', 0.0):.4f}"
            )

            print()

    # =====================================================
    # AI RECOMMENDATION
    # =====================================================

    print("=" * 80)
    print("AI GENERATED RECOMMENDATION")
    print("=" * 80)

    recommendation = result.get(
        "ai_recommendation",
        None,
    )

    if recommendation:

        if isinstance(
            recommendation,
            dict,
        ):

            print(
                f"\nProduct ID : "
                f"{recommendation.get('product_id')}"
            )

            print(
                f"Title      : "
                f"{recommendation.get('title')}"
            )

            print(
                f"Reason     : "
                f"{recommendation.get('reason')}"
            )

            print(
                f"Confidence : "
                f"{recommendation.get('confidence')}"
            )

        else:

            print(
                recommendation
            )

    else:

        print(
            "No recommendation generated."
        )

    # =====================================================
    # COMPLETE STATE
    # =====================================================

    print("\n")
    print("=" * 80)
    print("V2 TEST COMPLETE")
    print("=" * 80)

finally:

    db.close()

