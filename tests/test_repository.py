from app.database.session import SessionLocal
from app.repositories import user_repository
from app.schemas.user import UserCreate

db = SessionLocal()

user = UserCreate(
    username="testuser",
    email="test@example.com",
    password="password123"
)

created = user_repository.create_user(db, user)

print(created.id)
print(created.username)
print(created.email)

db.close()