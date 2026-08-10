from app.database.database import SessionLocal
from app.repositories.product_repository import product_repository
from app.services.qdrant_service import qdrant_service


db = SessionLocal()

try:

    # -----------------------------
    # PostgreSQL
    # -----------------------------

    products = product_repository.get_all(db)

    postgres_ids = {
        product.id
        for product in products
    }

    embedded_flag_ids = {
        product.id
        for product in products
        if product.embedding_generated
    }

    # -----------------------------
    # Qdrant
    # -----------------------------

    points = qdrant_service.client.scroll(
        collection_name=qdrant_service.collection_name,
        limit=100,
        with_payload=True,
        with_vectors=False,
    )[0]

    qdrant_ids = {
        int(point.id)
        for point in points
    }

    # -----------------------------
    # Comparison
    # -----------------------------

    print("\n" + "=" * 70)
    print("POSTGRESQL vs QDRANT")
    print("=" * 70)

    print(
        f"PostgreSQL products       : "
        f"{len(postgres_ids)}"
    )

    print(
        f"PostgreSQL marked embedded: "
        f"{len(embedded_flag_ids)}"
    )

    print(
        f"Qdrant points             : "
        f"{len(qdrant_ids)}"
    )

    print("\nPostgreSQL IDs:")
    print(sorted(postgres_ids))

    print("\nQdrant IDs:")
    print(sorted(qdrant_ids))

    # -----------------------------
    # Exists in Qdrant but not PG
    # -----------------------------

    qdrant_only = qdrant_ids - postgres_ids

    print("\nQDRANT ONLY:")
    print(sorted(qdrant_only))

    # -----------------------------
    # Exists in PG but not Qdrant
    # -----------------------------

    postgres_only = postgres_ids - qdrant_ids

    print("\nPOSTGRESQL ONLY:")
    print(sorted(postgres_only))

    # -----------------------------
    # PG says false but Qdrant exists
    # -----------------------------

    flag_mismatch = (
        qdrant_ids & postgres_ids
    ) - embedded_flag_ids

    print(
        "\nQDRANT EXISTS BUT "
        "POSTGRESQL FLAG IS FALSE:"
    )

    print(sorted(flag_mismatch))

finally:

    db.close()