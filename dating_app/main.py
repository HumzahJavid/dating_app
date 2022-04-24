from pathlib import Path

from fastapi import APIRouter, FastAPI, Form, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import dating_app.services as services
from dating_app.db.database import MongoDB
from dating_app.schemas.User import (
    RegisterResponse,
    RegisterResponse201,
    RegisterResponse409,
    UserCreate,
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


@api_router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    return {
        f"email: {email}, password: {password}",
    }


@api_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse,
    responses={
        "201": {"model": RegisterResponse201},
        "409": {"model": RegisterResponse409},
    },
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


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8001, reload=True, access_log=False)
