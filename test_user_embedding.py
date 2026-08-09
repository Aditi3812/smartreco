from app.database.database import SessionLocal

from app.services.recommendation_context_service import (
    recommendation_context_service,
)

from app.services.user_embedding_service import (
    user_embedding_service,
)


db = SessionLocal()

try:

    user_id = 3

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

    text, embedding = (
        user_embedding_service
        .generate_user_embedding(
            behavior_profile,
            top_products,
        )
    )

    print("\n")
    print("=" * 80)
    print("USER PREFERENCE TEXT")
    print("=" * 80)

    print(text)

    print("\n")
    print("=" * 80)
    print("USER EMBEDDING")
    print("=" * 80)

    print(
        "Dimensions:",
        len(embedding),
    )

    print(
        "First 10 values:",
        embedding[:10],
    )

finally:

    db.close()