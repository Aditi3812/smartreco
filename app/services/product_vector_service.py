from qdrant_client.models import PointStruct

from app.vector_db.qdrant import (
    qdrant_client,
    COLLECTION_NAME,
)

from app.services.embedding_service import (
    embedding_service,
)


class ProductVectorService:

    def index_product(self, product):

        embedding = (
            embedding_service
            .generate_product_embedding(
                product
            )
        )

        payload = {
            "product_id": product.id,
            "title": product.title,
            "category": product.category,
            "difficulty": product.difficulty,
            "language": product.language,
            "price": float(product.price)
            if product.price is not None
            else None,
            "skills": product.skills,
            "tags": product.tags,
        }

        point = PointStruct(
            id=product.id,
            vector=embedding,
            payload=payload,
        )

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point],
        )

        return point


product_vector_service = (
    ProductVectorService()
)