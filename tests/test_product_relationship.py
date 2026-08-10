from app.database.database import SessionLocal
from app.models.product_interaction import ProductInteraction


db = SessionLocal()

try:

    interaction = (
        db.query(ProductInteraction)
        .filter(
            ProductInteraction.user_id == 3
        )
        .first()
    )

    if not interaction:

        print("No product interaction found.")

    else:

        print("=" * 60)
        print("PRODUCT RELATIONSHIP TEST")
        print("=" * 60)

        print(
            "Interaction ID:",
            interaction.id,
        )

        print(
            "Product ID:",
            interaction.product_id,
        )

        print(
            "Product:",
            interaction.product,
        )

        if interaction.product:

            print(
                "Product title:",
                interaction.product.title,
            )

            print(
                "Product category:",
                interaction.product.category,
            )

        else:

            print(
                "ERROR: Product relationship returned None"
            )

finally:

    db.close()