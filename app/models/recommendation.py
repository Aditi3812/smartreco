
from datetime import datetime, UTC

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Recommendation(Base):

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    behavioral_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    semantic_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    preference_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    final_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )
