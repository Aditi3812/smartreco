from app.database.database import SessionLocal

from app.repositories.product_interaction_repository import (
    product_interaction_repository,
)


db = SessionLocal()

try:

    user_id = 3
    product_id = 1

    interaction = (
        product_interaction_repository.get_or_create(
            db,
            user_id,
            product_id,
        )
    )

    print("\n===== PRODUCT INTERACTION =====")

    print(
        "Interaction ID:",
        interaction.id,
    )

    print(
        "User ID:",
        interaction.user_id,
    )

    print(
        "Product ID:",
        interaction.product_id,
    )

    print(
        "View Count:",
        interaction.view_count,
    )

    print(
        "Interaction Score:",
        interaction.interaction_score,
    )

finally:

    db.close()