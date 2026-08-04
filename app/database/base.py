from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

# Import models here so SQLAlchemy metadata knows about them
from app.models.user import User