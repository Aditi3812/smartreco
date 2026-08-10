from app.vector_db.qdrant import (
    qdrant_client,
    COLLECTION_NAME,
)


result = qdrant_client.scroll(
    collection_name=COLLECTION_NAME,
    limit=20,
    with_payload=True,
    with_vectors=False,
)

points = result[0]

print("\n")
print("=" * 80)
print("                  QDRANT PRODUCTS")
print("=" * 80)

for point in points:

    payload = point.payload

    print(
        f"\nQdrant ID: {point.id}"
    )

    print(
        f"Product ID: "
        f"{payload.get('product_id')}"
    )

    print(
        f"Title: "
        f"{payload.get('title')}"
    )

    print(
        f"Category: "
        f"{payload.get('category')}"
    )

    print(
        f"Difficulty: "
        f"{payload.get('difficulty')}"
    )

    print(
        f"Language: "
        f"{payload.get('language')}"
    )

print("\n")
print("=" * 80)