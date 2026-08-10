from app.database.database import SessionLocal
from app.models.product import Product
from app.services.product_interaction_service import (
    product_interaction_service,
)

db = SessionLocal()

try:

    user_id = 3

    interactions = (
        product_interaction_service.build_interactions(
            db,
            user_id,
        )
    )

    print("\n")
    print("=" * 120)
    print("                    PRODUCT INTERACTION PROFILE")
    print("=" * 120)

    print(
        f"{'ID':<5}"
        f"{'PRODUCT':<30}"
        f"{'VIEWS':<8}"
        f"{'TIME':<12}"
        f"{'SCROLL':<10}"
        f"{'SEARCH':<10}"
        f"{'SCORE':<10}"
        f"{'RECENCY':<10}"
        f"{'FINAL':<10}"
    )

    print("-" * 120)

    for interaction in interactions:

        product = (
            db.query(Product)
            .filter(
                Product.id
                == interaction.product_id
            )
            .first()
        )

        product_title = (
            product.title
            if product
            else "Unknown Product"
        )

        print(
            f"{interaction.product_id:<5}"
            f"{product_title[:28]:<30}"
            f"{interaction.view_count:<8}"
            f"{interaction.total_time_spent:<12.1f}"
            f"{interaction.max_scroll_depth:<10.1f}"
            f"{interaction.search_count:<10}"
            f"{interaction.interaction_score:<10.3f}"
            f"{interaction.recency_score:<10.3f}"
            f"{interaction.final_score:<10.3f}"
        )

    print("=" * 120)

    print(
        f"Total products interacted with: "
        f"{len(interactions)}"
    )

    print("=" * 120)

finally:

    db.close()