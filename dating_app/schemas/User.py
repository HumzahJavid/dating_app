from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from dating_app.schemas.MongoModel import MongoModel


class UserModel(MongoModel):
    email: EmailStr = Field(...)
    password: str
    is_active: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {"email": "jdoe@example.com", "password": "mY=HvTb8@p3MhqKB"}
        }


# the fields from post request
class UserCreate(UserModel):
    confirmed_password: str


# any none id field optional
class UserUpdate(MongoModel):
    email: Optional[EmailStr]
    password: Optional[str]


class Gender(str, Enum):
    female = "female"
    male = "male"
    not_given = "not_given"
    other = "other"


class UserPublic(MongoModel):
    name: str = "Jane Doe"
    email: EmailStr
    age: Optional[int] = Field(
        25,
        gt=17,
        lt=65,
    )

    gender: Gender = Field("not_given")


class UserSearch(MongoModel):
    search_type: str
    name: Optional[str] = "Jane Doe"
    email: Optional[EmailStr]
    min_age: Optional[int] = Field(
        gt=17,
        lt=65,
    )
    max_age: Optional[int] = Field(
        gt=17,
        lt=65,
    )

    gender: Optional[Gender] = Field("not_given")


class RegisterResponse(BaseModel):
    message: str
    email: str = "jdoe@example.com"


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
    email: Optional[str]


class LoginResponse200(LoginResponse):
    message = "Login successful."
    email: str


class LoginResponse401(LoginResponse):
    message = "Invalid credentials."


class LoginResponseBase(LoginResponse):
    class Config:
        schema_extra = {
            "200": {"model": LoginResponse200},
            "401": {"model": LoginResponse401},
        }
