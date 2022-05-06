from bson import ObjectId
from fastapi import Body
from pydantic import BaseModel, Field


# https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/#the-_id-attribute-and-objectids
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


class MongoModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class InitiateChat(MongoModel):
    user_initiating_id: str = Body(...)
    user_receiving_id: str = Body(...)

    class Config:
        schema_extra = {
            "example": {
                "user_initiating_id": "jdoe@example.com",
                "user_receiving_id": "alice@example.com",
            }
        }


class InitiateChatResponse(BaseModel):
    chat_session_id: str

    class Config:
        schema_extra = {
            "example": {
                "chat_session_id": "jdoe@example.com-alice@example.com",
            }
        }
