from app.database.database import SessionLocal
from app.repositories.product_repository import product_repository
from app.services.qdrant_service import qdrant_service


db = SessionLocal()

try:
    # -----------------------------
    # PostgreSQL
    # -----------------------------

    products = product_repository.get_all(db)

    print("\n" + "=" * 70)
    print("POSTGRESQL")
    print("=" * 70)

    print(f"Products in PostgreSQL: {len(products)}")

    embedded_products = [
        product
        for product in products
        if product.embedding_generated
    ]

    print(
        f"Products marked embedded: "
        f"{len(embedded_products)}"
    )

    # -----------------------------
    # Qdrant
    # -----------------------------

    print("\n" + "=" * 70)
    print("QDRANT")
    print("=" * 70)

    collection_info = (
        qdrant_service.client
        .get_collection(
            qdrant_service.collection_name
        )
    )

    print(
        f"Points in Qdrant: "
        f"{collection_info.points_count}"
    )

    # -----------------------------
    # Compare
    # -----------------------------

    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)

    postgres_ids = {
        product.id
        for product in products
        if product.embedding_generated
    }

    qdrant_points = (
        qdrant_service.client
        .retrieve(
            collection_name=(
                qdrant_service.collection_name
            ),
            ids=list(postgres_ids),
        )
    )

    qdrant_ids = {
        point.id
        for point in qdrant_points
    }

    missing_from_qdrant = (
        postgres_ids - qdrant_ids
    )

    print(
        f"Embedded PostgreSQL products: "
        f"{len(postgres_ids)}"
    )

    print(
        f"Found in Qdrant: "
        f"{len(qdrant_ids)}"
    )

    print(
        f"Missing from Qdrant: "
        f"{len(missing_from_qdrant)}"
    )

    if missing_from_qdrant:
        print("\n❌ Missing product IDs:")
        print(sorted(missing_from_qdrant))

    else:
        print(
            "\n✅ ALL PRODUCT EMBEDDINGS "
            "ARE PRESENT IN QDRANT"
        )

finally:
    db.close()