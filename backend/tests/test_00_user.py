import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import UserDB, UserPublic
from app.db.repositories.users import UsersRepository
from app.services import auth_service

pytestmark = pytest.mark.asyncio


class TestUserRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        new_user = {
            "email": "test@email.io",
            "username": "test_username",
            "password": "testpassword",
        }
        res = await client.post(
            app.url_path_for("users:register-new-user"), json=new_user
        )
        assert res.status_code != HTTP_404_NOT_FOUND


class TestUserRegistration:
    async def test_users_can_register_successfully(
        self,
        app: FastAPI,
        client: AsyncClient,
        db: AsyncIOMotorDatabase,
    ) -> None:
        user_repo = UsersRepository(db)
        new_user = {
            "email": "shakira@shakira.io",
            "username": "abc",
            "password": "testing",
        }
        # make sure user doesn't exist yet
        user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
        assert user_in_db is None

        # send post request to create user and ensure it is successful
        res = await client.post(
            app.url_path_for("users:register-new-user"), json=new_user
        )
        assert res.status_code == HTTP_201_CREATED
        # ensure that the user now exists in the db
        user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
        assert user_in_db is not None
        assert user_in_db.email == new_user["email"]
        assert user_in_db.username == new_user["username"]
        # check that the user returned in the response is equal to the user in the database
        created_user = UserPublic(**res.json()).dict(exclude={"access_token"})
        assert created_user == user_in_db.dict(exclude={"password", "salt"})

    @pytest.mark.parametrize(
        "attr, value, status_code",
        (
            ("email", "denislour@abc.io", 201),
            ("username", "denislour", 201),
            ("email", "invalid_email@one@two.io", 422),
            ("password", "short", 422),
            ("username", "acs@#$%^<>", 422),
            ("username", "ab", 422),
        ),
    )
    async def test_user_registration_fails_when_credentials_are_taken(
        self,
        app: FastAPI,
        client: AsyncClient,
        attr: str,
        value: str,
        status_code: int,
    ) -> None:
        new_user = {
            "email": "nottaken@email.io",
            "username": "not_taken_username",
            "password": "freepassword",
        }
        new_user[attr] = value
        res = await client.post(
            app.url_path_for("users:register-new-user"), json=new_user
        )
        assert res.status_code == status_code

    async def test_users_save_password_is_hashed_and_has_salt(
        self,
        app: FastAPI,
        client: AsyncClient,
        db: AsyncIOMotorDatabase,
    ) -> None:
        user_repo = UsersRepository(db)
        new_users = {
            "email": "testemail@gmail.com",
            "username": "testusername",
            "password": "testpassword",
        }

        # send post request to create user and ensure it is successful
        res = await client.post(
            app.url_path_for("users:register-new-user"), json=new_users
        )
        assert res.status_code == HTTP_201_CREATED

        # ensure that the users password is hashed in the db
        # and that we can verify it using our auth service
        user_in_db = await user_repo.get_user_by_email(email=new_users.get("email"))
        assert user_in_db is not None
        assert user_in_db.salt is not None and user_in_db.salt != "123"
        assert auth_service.verify_password(
            password=new_users.get("password"),
            salt=user_in_db.salt,
            hashed_pwd=user_in_db.password,
        )
