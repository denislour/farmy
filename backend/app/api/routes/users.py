from fastapi import Depends, APIRouter, Body
from starlette.status import HTTP_201_CREATED

from app.api.dependencies.db import get_repository
from app.models.user import UserCreate, UserPublic
from app.db.repositories.users import UsersRepository
from app.models.token import AccessToken
from app.services import auth_service

router = APIRouter()


@router.post(
    "/",
    response_model=UserPublic,
    name="users:register-new-user",
    status_code=HTTP_201_CREATED,
)
async def register_new_user(
    new_user: UserCreate,
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserPublic:
    created_user = await user_repo.register_new_user(new_user=new_user)
    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=created_user),
        token_type="bearer",
    )
    created_user_params = created_user.copy(update={"_id": str(created_user.id)})
    return UserPublic(
        **created_user_params.dict(exclude={"id"}),
        access_token=access_token,
        id=str(created_user.id)
    )
