from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


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


class UserModel(MongoModel):
    email: EmailStr = Field(...)
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
            }
        }


# the fields from post request
class UserCreate(UserModel):
    confirmed_password: str


# any none id field optional
class UserUpdate(MongoModel):
    email: Optional[EmailStr]
    password: Optional[str]


class RegisterResponse(BaseModel):
    message: str
    email: str = "jdoe.example.com"


class RegisterResponse201(RegisterResponse):
    message = "Created user with email."


class RegisterResponse409(RegisterResponse):
    message = "Email already in use."


class RegisterResponseBase(RegisterResponse):
    class Config:
        schema_extra = {
            "201": {"model": RegisterResponse201},
            "409": {"model": RegisterResponse409},
        }


class LoginResponse(BaseModel):
    message: str


class LoginResponse200(LoginResponse):
    message = "Login successful."


class LoginResponse401(LoginResponse):
    message = "Invalid credentials."


class LoginResponseBase(LoginResponse):
    class Config:
        schema_extra = {
            "200": {"model": LoginResponse200},
            "401": {"model": LoginResponse401},
        }
