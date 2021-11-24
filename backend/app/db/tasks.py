from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
import logging


logger = logging.getLogger(__name__)
settings = get_settings()


async def connect_to_db(app: FastAPI) -> None:
    try:
        app.state._db_client = AsyncIOMotorClient(
            settings.DB_URL, tls=True, tlsAllowInvalidCertificates=True
        )
        app.state._db = app.state._db_client[settings.DB_NAME]
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
