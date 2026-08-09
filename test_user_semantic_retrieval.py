from app.database.database import SessionLocal

from app.services.recommendation_context_service import (
    recommendation_context_service,
)

from app.services.semantic_retrieval_service import (
    semantic_retrieval_service,
)

from app.models.product import Product


db = SessionLocal()

try:

    user_id = 3

    # -----------------------------------------
    # Build user context
    # -----------------------------------------

    context = (
        recommendation_context_service
        .build_context(
            db,
            user_id,
        )
    )

    behavior_profile = (
        context["behavior_profile"]
    )

    top_products = (
        context["top_products"]
    )

    # -----------------------------------------
    # Semantic retrieval
    # -----------------------------------------

    retrieval = (
        semantic_retrieval_service
        .retrieve_for_user(
            db=db,
            user_id=user_id,
            behavior_profile=behavior_profile,
            top_products=top_products,
            limit=5,
        )
    )

    print("\n")
    print("=" * 90)
    print("             USER SEMANTIC RETRIEVAL")
    print("=" * 90)

    print("\nUSER PREFERENCE TEXT:")
    print("-" * 90)

    print(
        retrieval["preference_text"]
    )

    print("\n")
    print("SEMANTICALLY RELEVANT PRODUCTS:")
    print("-" * 90)

    for rank, result in enumerate(
        retrieval["results"],
        start=1,
    ):

        product_id = result.id
        score = result.score

        product = (
            db.query(Product)
            .filter(
                Product.id == product_id
            )
            .first()
        )

        if product:

            print(
                f"{rank:<5}"
                f"{product.id:<5}"
                f"{product.title:<35}"
                f"Score: {score:.4f}"
            )

    print("=" * 90)

finally:

    db.close()