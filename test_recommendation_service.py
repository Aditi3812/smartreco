from app.database.database import SessionLocal

from app.services.recommendation_service import (
    recommendation_service,
)


db = SessionLocal()

try:

    user_id = 3

    recommendations = (
        recommendation_service
        .generate_recommendations(
            db,
            user_id,
            limit=5,
        )
    )

    print("\n")

    print("=" * 100)

    print(
        "              SMARTRECO RECOMMENDATIONS"
    )

    print("=" * 100)

    print(
        f"{'RANK':<6}"
        f"{'ID':<6}"
        f"{'PRODUCT':<30}"
        f"{'BEHAVIOR':<12}"
        f"{'SEMANTIC':<12}"
        f"{'PREFERENCE':<12}"
        f"{'FINAL':<10}"
    )

    print("-" * 100)

    for rank, item in enumerate(
        recommendations,
        start=1,
    ):

        product = item["product"]

        print(
            f"{rank:<6}"
            f"{product.id:<6}"
            f"{product.title[:28]:<30}"
            f"{item['behavioral_score']:<12.4f}"
            f"{item['semantic_score']:<12.4f}"
            f"{item['preference_score']:<12.4f}"
            f"{item['final_score']:<10.4f}"
        )

    print("=" * 100)

finally:

    db.close()