from datetime import datetime, UTC

from sqlalchemy.orm import Session

from app.models.product_interaction import ProductInteraction


class ProductInteractionRepository:
    """
    Handles database operations
    for product-level user interactions.
    """

    def get_by_user_and_product(
        self,
        db: Session,
        user_id: int,
        product_id: int,
    ):
        return (
            db.query(ProductInteraction)
            .filter(
                ProductInteraction.user_id == user_id,
                ProductInteraction.product_id == product_id,
            )
            .first()
        )

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(ProductInteraction)
            .filter(
                ProductInteraction.user_id == user_id
            )
            .all()
        )

    def create(
        self,
        db: Session,
        user_id: int,
        product_id: int,
    ):

        interaction = ProductInteraction(
            user_id=user_id,
            product_id=product_id,
            view_count=0,
            total_time_spent=0,
            max_scroll_depth=0,
            search_count=0,
            interaction_score=0,
            last_interacted_at=datetime.now(UTC),
        )

        db.add(interaction)
        db.flush()
        db.refresh(interaction)

        return interaction

    def get_or_create(
        self,
        db: Session,
        user_id: int,
        product_id: int,
    ):

        interaction = (
            self.get_by_user_and_product(
                db,
                user_id,
                product_id,
            )
        )

        if interaction:
            return interaction

        return self.create(
            db,
            user_id,
            product_id,
        )

    def update(
        self,
        db: Session,
        interaction: ProductInteraction,
    ):

        interaction.last_interacted_at = (
            datetime.now(UTC)
        )

        db.flush()
        db.refresh(interaction)

        return interaction
    def get_top_by_user(
        self,
        db: Session,
        user_id: int,
        limit: int = 10,
    ):
        return (
            db.query(ProductInteraction)
            .filter(
                ProductInteraction.user_id == user_id
            )
            .order_by(
                ProductInteraction.final_score.desc()
            )
            .limit(limit)
            .all()
        )


product_interaction_repository = (
    ProductInteractionRepository()
)