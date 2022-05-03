from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, FastAPI, Form, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

import dating_app.services as services
from dating_app.db.database import MongoDB
from dating_app.schemas.User import (
    LoginResponse,
    LoginResponseBase,
    RegisterResponse,
    RegisterResponseBase,
    UserCreate,
    UserModel,
    UserPublic,
    UserSearch,
)

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_PATH / "templates")


app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_PATH / "static"), name="static")
api_router = APIRouter()
mongo = MongoDB()


@app.on_event("startup")
async def startup_db_client() -> None:
    global mongo
    await mongo.startup_db_client()


@app.on_event("shutdown")
async def shutdown_db_client() -> None:
    global mongo
    await mongo.shutdown_db_client()


# @app.get("/")
@api_router.get("/", status_code=200)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@api_router.get("/items/{item_id}")
async def read_item(request: Request, item_id: int):
    return templates.TemplateResponse(
        "items.html", {"request": request, "item_id": item_id}
    )


# @app.get("/")
@api_router.get("/searchpage", status_code=200)
async def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@api_router.post(
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
    login_response = await services.authenticate_user(mongo.mongodb, user_form)
    print(f"user is {login_response}")
    if "Invalid" in login_response.message:
        print(f"Invalid credentials 401: {email}")
        response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.set_cookie(key="X-Authorization", value=email, httponly=True)

    return login_response


@api_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    logout_response = await services.logout(mongo.mongodb)
    print(logout_response)
    return logout_response


@api_router.post(
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
    register_response = await services.create_user(mongo.mongodb, user)

    if "already in use." in register_response.message:
        response.status_code = status.HTTP_409_CONFLICT

    return register_response


@api_router.get(
    "/all", response_description="List all other Users", response_model=List[UserPublic]
)
async def list_all():
    all_users = await services.list_users(mongo.mongodb)
    return all_users


@api_router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_description="Search for other Users",
)
async def search(
    search_type: str,
    email: Optional[str] = None,
    name: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    gender: Optional[str] = None,
):

    # Convert potential empty string variables to None.
    # None is more compatible with mongo than empty strings
    fields = [email, name, gender]
    # https://stackoverflow.com/questions/4260280/if-else-in-a-list-comprehension
    processed_fields = [element if element else None for element in fields]
    email, name, gender = processed_fields
    # if search by email, redirect to find_one by email endpoint?

    # initialise to run server side validation
    search_criteria: UserSearch = UserSearch(
        search_type=search_type,
        name=name,
        email=email,
        min_age=min_age,
        max_age=max_age,
        gender=gender,
    )

    found_users = await services.search_users(mongo.mongodb, search_criteria)
    response = {"data": found_users, "length": len(found_users)}
    return response


@api_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_description="View active users profile",
)
async def view_user_me(request: Request):
    current_user = await services.get_current_user(mongo.mongodb)
    return templates.TemplateResponse(
        "edit_profile.html", {"request": request, "user": current_user}
    )


@api_router.put(
    "/me",
    status_code=status.HTTP_200_OK,
    response_description="Edit active users profile",
)
async def update_user_me(
    # *,
    email: Optional[EmailStr] = Form(None),
    password: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    age: Optional[int] = Form(None),
    gender: Optional[str] = Form(None),
) -> Any:
    """
    Update own user.
    """
    user_in: Dict[str, Any] = {}
    if email is not None:
        user_in["email"] = email
    if password is not None:
        user_in["password"] = password
    if name is not None:
        user_in["name"] = name
    if age is not None:
        user_in["age"] = age
    if gender is not None:
        user_in["gender"] = gender

    current_user = await services.get_current_user(mongo.mongodb)
    update_response = await services.update_user(mongo.mongodb, current_user, user_in)
    return update_response


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8001, reload=True, access_log=False)
