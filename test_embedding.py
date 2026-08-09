from app.database.database import SessionLocal
from app.models.product import Product

from app.services.embedding_service import (
    embedding_service,
)


db = SessionLocal()

try:

    product = (
        db.query(Product)
        .filter(Product.id == 1)
        .first()
    )

    if not product:

        print("Product not found")

    else:

        print("\n==============================")
        print("PRODUCT")
        print("==============================")

        print("ID:", product.id)
        print("Title:", product.title)

        text = (
            embedding_service
            .build_product_text(product)
        )

        print("\n==============================")
        print("SEMANTIC TEXT")
        print("==============================")

        print(text)

        embedding = (
            embedding_service
            .generate_product_embedding(
                product
            )
        )

        print("\n==============================")
        print("EMBEDDING")
        print("==============================")

        print(
            "Vector dimensions:",
            len(embedding)
        )

        print(
            "First 10 values:",
            embedding[:10]
        )

finally:

    db.close()