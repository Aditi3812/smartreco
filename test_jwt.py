from app.services.jwt_service import jwt_service

token = jwt_service.create_access_token(
    {
        "sub": "1",
        "email": "test@example.com",
        "role": "user",
    }
)

print("Generated Token:\n")
print(token)

print("\nDecoded Payload:\n")
print(jwt_service.verify_token(token))