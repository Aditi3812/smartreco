
from app.database.database import SessionLocal

from app.repositories.behavior_profile_repository import (
    behavior_profile_repository,
)

from app.repositories.product_interaction_repository import (
    product_interaction_repository,
)

from app.repositories.product_repository import (
    product_repository,
)

from app.services.semantic_retrieval_service import (
    semantic_retrieval_service,
)

from app.services.hybrid_ranking_service import (
    hybrid_ranking_service,
)


db = SessionLocal()

try:

    user_id = 3

    # ---------------------------------------
    # Get behavior profile
    # ---------------------------------------

    behavior_profile = (
        behavior_profile_repository.get_by_user_id(
            db,
            user_id,
        )
    )

    # ---------------------------------------
    # Get user interactions
    # ---------------------------------------

    interactions = (
        product_interaction_repository.get_by_user(
            db,
            user_id,
        )
    )

    # ---------------------------------------
    # Top interacted products
    # ---------------------------------------

    top_products = interactions[:5]

    # ---------------------------------------
    # Semantic retrieval
    # ---------------------------------------

    semantic_data = (
        semantic_retrieval_service.retrieve_for_user(
            db,
            user_id,
            behavior_profile,
            top_products,
            limit=10,
        )
    )

    semantic_results = semantic_data["results"]

    # ---------------------------------------
    # Build semantic score lookup
    # ---------------------------------------

    semantic_scores = {
        result.payload["product_id"]: result.score
        for result in semantic_results
    }

    print("\nSEMANTIC RAW RESULTS:")
    print(semantic_results)

    # ---------------------------------------
    # Get interacted product IDs
    # ---------------------------------------

    interacted_ids = {
        interaction.product_id
        for interaction in interactions
    }

    # ---------------------------------------
    # Get all products
    # ---------------------------------------

    products = product_repository.get_all(
        db
    )

    # ---------------------------------------
    # Build behavioral score lookup
    # ---------------------------------------

    behavioral_scores = {
        interaction.product_id: interaction.final_score
        for interaction in interactions
    }

    # ---------------------------------------
    # Build candidates
    # ---------------------------------------

    candidates = []

    for product in products:

        # Don't recommend already
        # interacted products for now.
        if product.id in interacted_ids:
            continue

        candidates.append(
            {
                "product": product,

                "behavioral_score": behavioral_scores.get(
                    product.id,
                    0.0,
                ),

                "semantic_score": semantic_scores.get(
                    product.id,
                    0.0,
                ),
            }
        )

    # ---------------------------------------
    # HYBRID RANKING
    # ---------------------------------------

    ranked = (
        hybrid_ranking_service.rank_candidates(
            candidates,
            behavior_profile,
        )
    )

    # ---------------------------------------
    # Print results
    # ---------------------------------------

    print("\n")
    print("=" * 100)
    print("                 HYBRID RECOMMENDATION RANKING")
    print("=" * 100)

    print(
        f"{'RANK':<6}"
        f"{'ID':<6}"
        f"{'PRODUCT':<30}"
        f"{'BEHAVIOR':<12}"
        f"{'SEMANTIC':<12}"
        f"{'PREFERENCE':<12}"
        f"{'FINAL':<10}"
    )

    print("-" * 100)

    for rank, item in enumerate(
        ranked,
        start=1,
    ):

        product = item["product"]

        print(
            f"{rank:<6}"
            f"{product.id:<6}"
            f"{product.title[:28]:<30}"
            f"{item['behavioral_score']:<12.4f}"
            f"{item['semantic_score']:<12.4f}"
            f"{item['preference_score']:<12.4f}"
            f"{item['final_score']:<10.4f}"
        )

    print("=" * 100)

finally:

    db.close()

