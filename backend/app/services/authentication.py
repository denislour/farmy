import jwt
import bcrypt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.core.config import settings
from app.models.user import UserPasswordUpdate, UserDB
from app.models.token import JWTMeta, JWTCreds, JWTPayload


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on.
    """

    pass


class AuthService:
    def create_salt_and_hashed_password(
        self, *, plaintext_password: str
    ) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=plaintext_password, salt=salt)
        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, *, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    def verify_password(self, *, password: str, salt: str, hashed_pwd: str) -> bool:
        return pwd_context.verify(password + salt, hashed_pwd)

    def create_access_token_for_user(
        self,
        *,
        user: UserDB,
        secret_key: str = settings.secret_key,
        audience: str = settings.jwt_audience,
        expires_in: int = settings.access_token_expire_minutes
    ) -> str:
        if not user or not isinstance(user, UserDB):
            return None
        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
        )
        jwt_creds = JWTCreds(sub=user.email, username=user.username)
        token_payload = JWTPayload(**jwt_meta.dict(), **jwt_creds.dict())

        access_token = jwt.encode(
            token_payload.dict(), secret_key, algorithm=settings.jwt_algorithm
        )
        return access_token
