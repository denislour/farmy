from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Base(BaseModel):
    """
    Any common logic to be shared by all models goes here.
    """

    pass


class IDModelMixin(BaseModel):
    id: PyObjectId = Field(..., default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
