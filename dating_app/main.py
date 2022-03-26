from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_PATH / "templates")


app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_PATH / "static"), name="static")
api_router = APIRouter()


# @app.get("/")
@api_router.get("/", status_code=200)
async def root() -> None:
    return {"message": "Hello World"}


@api_router.get("/items/{item_id}")
async def read_item(request: Request, item_id: int) -> dict:
    return templates.TemplateResponse(
        "items.html", {"request": request, "item_id": item_id}
    )


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8001, reload=True, access_log=False)
