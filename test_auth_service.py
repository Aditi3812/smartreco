from app.database.session import SessionLocal
from app.schemas.user import UserCreate
from app.services.auth_service import auth_service

db = SessionLocal()

# Use a unique username/email each time
user = UserCreate(
    username="aditi1",
    email="aditi1@example.com",
    password="HelloWorld123",
)

try:
    created = auth_service.register_user(db, user)

    print("User Created!")
    print(created.id)
    print(created.username)
    print(created.email)

except Exception as e:
    print(e)

print("\nTesting Login...")

logged_user = auth_service.authenticate_user(
    db,
    "aditi1@example.com",
    "HelloWorld123",
)

if logged_user:
    print("Login Successful!")
    print(logged_user.username)
else:
    print("Login Failed!")

db.close()