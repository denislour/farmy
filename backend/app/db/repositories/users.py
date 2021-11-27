from pydantic import EmailStr
from fastapi import HTTPException, status
from app.db.repositories.base import BaseRepository
from app.models.user import UserCreate, UserDB


class UsersRepository(BaseRepository):
    async def get_user_by_email(self, *, email: EmailStr) -> UserDB:
        user_record = await self.db.users.find_one({"email": email})
        if not user_record:
            return None
        return UserDB(**user_record)

    async def get_user_by_username(self, *, username: str) -> UserDB:
        user_record = await self.db.users.find_one({"username": username})
        if not user_record:
            return None
        return UserDB(**user_record)

    async def register_new_user(self, *, new_user: UserCreate) -> UserDB:
        # make sure email isn't already taken
        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That email is already taken. Login with that email or register with another one.",
            )
        # make sure username isn't already taken
        if await self.get_user_by_username(username=new_user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That username is already taken. Please try another one.",
            )
        created_user = await self.db.users.insert_one(new_user.dict())
        user_inserted = await self.db.users.find_one({"_id": created_user.inserted_id})
        return UserDB(**user_inserted)
