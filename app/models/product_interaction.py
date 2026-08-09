from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database.base import Base


class ProductInteraction(Base):

    __tablename__ = "product_interactions"
    __table_args__ = (
    UniqueConstraint(
        "user_id",
        "product_id",
        name="uq_user_product_interaction",
    ),
)
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
    )
    product = relationship(
        "Product",
        lazy="joined",
    )
    view_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    total_time_spent = Column(
        Float,
        default=0,
        nullable=False,
    )

    max_scroll_depth = Column(
        Float,
        default=0,
        nullable=False,
    )

    search_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    interaction_score = Column(
        Float,
        default=0,
        nullable=False,
    )

    last_interacted_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    recency_score = Column(
        Float,
        default=1.0,
    )
    final_score = Column(
        Float,
        default=0.0,
    )