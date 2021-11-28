from datetime import datetime, timedelta

from pydantic import EmailStr
from app.models.base import Base
from app.core.config import settings


class JWTMeta(Base):
    iss: str = "Farmy Issuer"
    aud: str = settings.jwt_audience
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    )


class JWTCreds(Base):
    """How we'll identify users"""

    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    """

    pass


class AccessToken(Base):
    access_token: str
    token_type: str
