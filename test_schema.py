from app.schemas.user import UserCreate

user = UserCreate(
    username="aditi",
    email="aditi@example.com",
    password="securepassword123"
)

print(user)