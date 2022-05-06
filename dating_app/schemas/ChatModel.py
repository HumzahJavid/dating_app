from fastapi import Body
from pydantic import BaseModel

from dating_app.schemas.MongoModel import MongoModel


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
