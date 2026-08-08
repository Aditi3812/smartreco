from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    JSON,
    ForeignKey,
)

from app.database.base import Base


class BehaviorProfile(Base):

    __tablename__ = "behavior_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    category_scores = Column(
        JSON,
        nullable=True,
    )

    difficulty_scores = Column(
        JSON,
        nullable=True,
    )

    language_scores = Column(
        JSON,
        nullable=True,
    )

    search_frequency = Column(
        Integer,
        default=0,
        nullable=False,
    )

    average_time_spent = Column(
        Float,
        default=0,
        nullable=False,
    )

    average_scroll_depth = Column(
        Float,
        default=0,
        nullable=False,
    )

    purchase_intent = Column(
        Float,
        default=0,
        nullable=False,
    )

    total_events = Column(
        Integer,
        default=0,
        nullable=False,
    )

    last_updated = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )