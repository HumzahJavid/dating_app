from fastapi import APIRouter, Form, Response, status

import dating_app.services as services
from dating_app.db import mongo
from dating_app.schemas.User import (
    LoginResponse,
    LoginResponseBase,
    RegisterResponse,
    RegisterResponseBase,
    UserCreate,
    UserModel,
)

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse,
    responses=RegisterResponseBase.Config.schema_extra,  # type: ignore
)
async def register(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    confirmPassword: str = Form(...),
):
    user = UserCreate(
        email=email, password=password, confirmed_password=confirmPassword
    )
    db = mongo.get_db()
    print(db["users"])

    register_response = await services.create_user(db, user)

    if "already in use." in register_response.message:
        response.status_code = status.HTTP_409_CONFLICT

    return register_response


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    responses=LoginResponseBase.Config.schema_extra,  # type: ignore
)
async def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
):

    user_form = UserModel(email=email, password=password)
    db = mongo.get_db()
    print(db["users"])
    login_response = await services.authenticate_user(db, user_form)
    print(f"user is {login_response}")
    if "Invalid" in login_response.message:
        print(f"Invalid credentials 401: {email}")
        response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.set_cookie(key="X-Authorization", value=email, httponly=True)

    return login_response


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    db = mongo.get_db()
    logout_response = await services.logout(db)
    print(logout_response)
    return logout_response
