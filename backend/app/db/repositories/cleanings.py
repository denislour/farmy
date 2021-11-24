from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningUpdate, CleaningIn


class CleaningsRepository(BaseRepository):
    """ "
    All database actions associated with the Cleaning resource
    """

    async def create_cleaning(self, *, new_cleaning: CleaningCreate) -> CleaningIn:
        cleaning = await self.engine["cleanings"].insert_one(new_cleaning.dict())
        cleaning_inserted = await self.engine["cleanings"].find_one(
            {"_id": cleaning.inserted_id}
        )
        return CleaningIn(**cleaning_inserted)
