from typing import Optional
from enum import Enum
from app.models.base import IDModelMixin, Base


class CleaningType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"


class CleaningBase(Base):
    """
    All common characteristics of our Cleaning resource
    """

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    cleaning_type: Optional[CleaningType] = "spot_clean"


class CleaningCreate(CleaningBase):
    """
    Attributes required to create a new resource - used at POST requests
    """

    name: str
    price: float


class CleaningUpdate(CleaningBase):
    """
    Attributes that can be updated - used at PUT requests
    """

    cleaning_type: Optional[CleaningType]


class CleaningIn(IDModelMixin, CleaningBase):
    """
    Attributes present on any resource coming out of the database
    """

    name: str
    price: float
    cleaning_type: CleaningType


class CleaningOut(IDModelMixin, CleaningBase):
    """
    Attributes present on public facing resources being returned from GET, POST, and PUT requests
    """

    pass
