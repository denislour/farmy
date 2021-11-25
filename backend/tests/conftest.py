import warnings
import os
from motor.motor_asyncio import AsyncIOMotorDatabase
import pytest

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from app.core.config import settings
from app.db.repositories.cleanings import CleaningsRepository
from app.models.cleaning import CleaningCreate
from app.models.cleaning import CleaningIn


async def teardown(db: AsyncIOMotorDatabase) -> None:
    db.cleanings.delete_many({})


@pytest.fixture
async def app() -> FastAPI:
    from app.api.server import get_application

    settings.testing = True
    return get_application()


@pytest.fixture
async def db(app: FastAPI) -> AsyncIOMotorDatabase:
    db = app.state._db
    yield db
    await teardown(db)


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture
async def test_cleaning(db: AsyncIOMotorDatabase) -> CleaningIn:
    cleaning_repo = CleaningsRepository(db)
    new_cleaning = CleaningCreate(
        name="fake cleaning name",
        description="fake cleaning description",
        price=9.99,
        cleaning_type="spot_clean",
    )
    return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning)


@pytest.fixture
async def new_cleaning() -> CleaningIn:
    return CleaningCreate(
        name="test cleaning",
        description="description",
        price=0.00,
        cleaning_type="spot_clean",
    )
