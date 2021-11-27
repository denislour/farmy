from typing import List
from pymongo import ReturnDocument
from pydantic.types import T

from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningIn, CleaningUpdate
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

    async def get_all_cleanings(self) -> List[CleaningIn]:
        cleanings = await self.db.cleanings.find().to_list(length=100)
        return [CleaningIn(**l) for l in cleanings]

    async def update_cleaning(
        self, *, id: PyObjectId, cleaning_update: CleaningUpdate
    ) -> CleaningIn:
        cleaning = await self.get_cleaning_by_id(id=id)
        if not cleaning:
            return None
        cleaning_params = cleaning.copy(update=cleaning_update.dict(exclude_unset=True))
        update_cleaning = await self.db.cleanings.find_one_and_update(
            {"_id": id},
            {
                "$set": cleaning_params.dict(),
            },
            return_document=ReturnDocument.AFTER,
        )
        return CleaningIn(**update_cleaning)

    async def delete_cleaning_by_id(self, *, id) -> int:
        deleted = await self.db.cleanings.find_one_and_delete({"_id": id})
        return deleted
