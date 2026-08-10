from app.database.database import SessionLocal
from app.models.product import Product
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service


db = SessionLocal()

try:

    product = (
        db.query(Product)
        .filter(Product.id == 1)
        .first()
    )

    if not product:
        print("Product not found")
        raise SystemExit

    print("\n")
    print("=" * 80)
    print("PRODUCT")
    print("=" * 80)

    print("ID:", product.id)
    print("Title:", product.title)

    # -----------------------------------------
    # Generate query embedding
    # -----------------------------------------

    embedding = (
        embedding_service
        .generate_product_embedding(product)
    )

    print("\nEmbedding dimensions:", len(embedding))

    # -----------------------------------------
    # Search Qdrant
    # -----------------------------------------

    results = (
        qdrant_service
        .search_products(
            query_embedding=embedding,
            limit=5,
        )
    )

    print("\n")
    print("=" * 80)
    print("SEMANTIC SEARCH RESULTS")
    print("=" * 80)

    for rank, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"{rank}. "
            f"Product ID: {result.id} "
            f"Score: {result.score:.4f}"
        )

finally:

    db.close()