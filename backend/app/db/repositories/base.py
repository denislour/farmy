from motor.motor_asyncio import AsyncIOMotorDatabase


class BaseRepository:
    def __init__(self, engine: AsyncIOMotorDatabase) -> None:
        self.engine = engine
