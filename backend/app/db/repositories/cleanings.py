from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningIn
from app.models.base import PyObjectId


class CleaningsRepository(BaseRepository):
    """ "
    All database actions associated with the Cleaning resource
    """

    async def create_cleaning(self, *, new_cleaning: CleaningCreate) -> CleaningIn:
        cleaning = await self.db.cleanings.insert_one(new_cleaning.dict())
        cleaning_inserted = await self.db.cleanings.find_one(
            {"_id": cleaning.inserted_id}
        )
        return CleaningIn(**cleaning_inserted)

    async def get_cleaning_by_id(self, *, id: PyObjectId) -> CleaningIn:
        cleaning = await self.db.cleanings.find_one({"_id": id})
        if not cleaning:
            return None
        return CleaningIn(**cleaning)
