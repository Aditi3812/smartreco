from datetime import datetime, timedelta, UTC
import jwt
import os
from dotenv import load_dotenv
from jose import JWTError
load_dotenv()


class JWTService:

    def __init__(self):

        self.secret_key = os.getenv("SECRET_KEY")

        self.algorithm = os.getenv("ALGORITHM")

        self.expire_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
        )

    def create_access_token(self, data: dict):

        payload = data.copy()

        expire = datetime.now(UTC) + timedelta(
            minutes=self.expire_minutes
        )

        payload.update(
            {
                "exp": expire
            }
        )

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )

    def verify_token(self, token: str):

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            return payload

        except JWTError:
            return None


jwt_service = JWTService()