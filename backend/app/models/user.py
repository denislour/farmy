import string
from typing import Optional
from pydantic import constr, EmailStr, validator
from app.models.base import DateTimeModelMixin, IDModelMixin, Base
from app.models.token import AccessToken


class UserBase(Base):
    """
    Leaving off password and salt from base model
    """

    email: Optional[EmailStr]
    username: Optional[str]
    email_verified: bool = False
    is_active: bool = False
    is_superuser: bool = False


class UserCreate(DateTimeModelMixin, Base):
    """
    Email, username, password are required for registering a new user
    """

    email: EmailStr
    password: constr(min_length=7, max_length=100)
    username: constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")


class UserUpdate(Base):
    """
    User are allow update their email and/or username
    """

    email: Optional[EmailStr]
    username: Optional[constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")]


class UserPasswordUpdate(Base):
    """
    User can change their password
    """

    password: constr(min_length=7, max_length=100)
    salt: str


class UserDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """

    password: constr(min_length=7, max_length=100)
    salt: Optional[str] = "password salt"


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    access_token: Optional[AccessToken]
