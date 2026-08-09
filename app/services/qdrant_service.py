from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


class QdrantService:

    def __init__(self):

        self.client = QdrantClient(
            host="localhost",
            port=6333,
        )

        self.collection_name = "smartreco_products"

    # -----------------------------------------
    # Store product embedding
    # -----------------------------------------

    def upsert_product(
        self,
        product_id: int,
        embedding: list[float],
        payload: dict,
    ):

        point = PointStruct(
            id=product_id,
            vector=embedding,
            payload=payload,
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

    # -----------------------------------------
    # Search similar products
    # -----------------------------------------

    def search_products(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
        )

        return results.points


qdrant_service = QdrantService()