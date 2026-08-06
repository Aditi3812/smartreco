from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.password_service import password_service
from app.services.jwt_service import jwt_service

class AuthService:
    """Handles user authentication business logic."""

    def __init__(self):
        self.user_repository = UserRepository()

    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str,
    ):
        """
        Authenticate a user.
        """

        user = self.user_repository.get_by_email(
            db,
            email,
        )

        if not user:
            return None

        valid = password_service.verify_password(
            password,
            user.password,
        )

        if not valid:
            return None

        return user
    def register_user(self, db: Session, user: UserCreate):
        """
        Register a new user.
        """

        # Check username
        existing_username = self.user_repository.get_by_username(
            db,
            user.username,
        )

        if existing_username:
            raise ValueError("Username already exists.")

        # Check email
        existing_email = self.user_repository.get_by_email(
            db,
            user.email,
        )

        if existing_email:
            raise ValueError("Email already registered.")

        # Hash password
        hashed_password = password_service.hash_password(
            user.password
        )

        # Replace plain password
        user.password = hashed_password

        # Save user
        created_user = self.user_repository.create_user(
            db,
            user,
        )

        return created_user
    


auth_service = AuthService()