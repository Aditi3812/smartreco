from app.services.password_service import password_service

password = "HelloWorld123"

hashed = password_service.hash_password(password)

print("Hash:", hashed)

print(
    password_service.verify_password(
        password,
        hashed,
    )
)