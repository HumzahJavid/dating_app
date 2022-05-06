from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, FastAPI, Form, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

import dating_app.services as services
from dating_app.api.chat import chat
from dating_app.api.user import user
from dating_app.core import websocket
from dating_app.db import mongo
from dating_app.schemas.User import UserPublic, UserSearch

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_PATH / "templates")


app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_PATH / "static"), name="static")
api_router = APIRouter()


@app.on_event("startup")
async def startup_db_client() -> None:
    await mongo.startup_db_client()


@app.on_event("shutdown")
async def shutdown_db_client() -> None:
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


api_router.include_router(websocket.router)
api_router.include_router(user.router, prefix="/api/user", tags=["user"])
api_router.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8001, reload=True, access_log=False)
