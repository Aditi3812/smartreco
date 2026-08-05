from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    """Handles all database operations related to users."""

    def create_user(self, db: Session, user: UserCreate) -> User:
        new_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def get_all_users(self, db: Session):
        return db.query(User).all()

    def delete_user(self, db: Session, user: User):
        db.delete(user)
        db.commit()