from app.vector_db.qdrant import qdrant_client


print("=" * 60)
print("QDRANT CONNECTION TEST")
print("=" * 60)

collections = qdrant_client.get_collections()

print("Qdrant connected successfully!")

print("\nCollections:")

for collection in collections.collections:
    print("-", collection.name)

print("=" * 60)