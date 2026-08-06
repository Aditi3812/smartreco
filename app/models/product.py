from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    difficulty: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(50),
        default="English",
    )

    duration: Mapped[int] = mapped_column(
        Integer,
    )

    price: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    instructor: Mapped[str] = mapped_column(
        String(100),
    )

    skills: Mapped[str] = mapped_column(
        String,
    )

    tags: Mapped[str] = mapped_column(
        String,
    )

    embedding_generated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )