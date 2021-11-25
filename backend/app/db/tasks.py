from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging


logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    settings.db_name = (
        f"{settings.db_name}_test"
        if settings.testing and not settings.db_name.endswith("_test")
        else settings.db_name
    )
    try:
        app.state._db_client = AsyncIOMotorClient(
            settings.db_url, tls=True, tlsAllowInvalidCertificates=True
        )
        app.state._db = app.state._db_client[settings.db_name]
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        app.state._db_client.close()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")
