from app.database.database import SessionLocal

from app.models.product import Product

from app.services.product_vector_service import (
    product_vector_service,
)


db = SessionLocal()

try:

    products = (
        db.query(Product)
        .order_by(Product.id)
        .all()
    )

    print("\n")
    print("=" * 80)
    print("              PRODUCT VECTOR INDEXING")
    print("=" * 80)

    print(
        f"Products found: {len(products)}"
    )

    print("-" * 80)

    for product in products:

        print(
            f"Indexing Product "
            f"{product.id}: "
            f"{product.title}"
        )

        product_vector_service.index_product(
            product
        )

        print("   ✓ Indexed")

    print("-" * 80)
    print("All products indexed successfully.")
    print("=" * 80)

finally:

    db.close()