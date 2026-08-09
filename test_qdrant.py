from app.vector_db.qdrant import qdrant_client

print("Connected to Qdrant")

print(
    qdrant_client.get_collections()
)