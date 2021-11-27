from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.cleaning import CleaningCreate, CleaningOut
from app.models.base import PyObjectId
from app.db.repositories.cleanings import CleaningsRepository
from app.api.dependencies.db import get_repository
from app.models.cleaning import CleaningOut, CleaningUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=CleaningOut,
    name="cleanings:create-cleaning",
    status_code=HTTP_201_CREATED,
)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningOut:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning)
    return created_cleaning


@router.get("/{id}/", response_model=CleaningOut, name="cleanings:get-cleaning-by-id")
async def get_cleaning_by_id(
    id: PyObjectId,
    cleaning_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningOut:
    cleaning = await cleaning_repo.get_cleaning_by_id(id=id)
    if not cleaning:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that id."
        )
    return cleaning


@router.get("/", response_model=List[CleaningOut], name="cleanings:get-all-cleanings")
async def get_all_cleanings(
    cleaning_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> List[CleaningOut]:
    return await cleaning_repo.get_all_cleanings()


@router.put(
    "/{id}/", response_model=CleaningOut, name="cleanings:update-cleaning-by-id"
)
async def update_cleaning_by_id(
    id: PyObjectId,
    cleaning_update: CleaningUpdate,
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningOut:
    updated_cleaning = await cleanings_repo.update_cleaning(
        id=id,
        cleaning_update=cleaning_update,
    )
    if not updated_cleaning:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No cleaning found with that id.",
        )
    return updated_cleaning


@router.delete("/{id}/", response_model=int, name="cleanings:delete-cleaning-by-id")
async def delete_cleaning_by_id(
    id: PyObjectId,
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> int:
    deleted = await cleanings_repo.delete_cleaning_by_id(id=id)
    if not deleted:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No cleaning found with that id.",
        )
    return 1
