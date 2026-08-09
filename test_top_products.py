from app.database.database import SessionLocal
from app.models.product import Product
from app.services.product_interaction_service import (
    product_interaction_service,
)

db = SessionLocal()

try:

    user_id = 3

    top_products = (
        product_interaction_service.get_top_products(
            db,
            user_id,
            limit=10,
        )
    )

    print("\n")
    print("=" * 100)
    print("                    TOP USER PRODUCTS")
    print("=" * 100)

    print(
        f"{'RANK':<7}"
        f"{'PRODUCT ID':<12}"
        f"{'PRODUCT':<30}"
        f"{'SCORE':<10}"
    )

    print("-" * 100)

    for rank, interaction in enumerate(
        top_products,
        start=1,
    ):

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
            f"{rank:<7}"
            f"{interaction.product_id:<12}"
            f"{product_title[:28]:<30}"
            f"{interaction.final_score:<10.3f}"
        )

    print("=" * 100)

finally:

    db.close()