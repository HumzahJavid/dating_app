from fastapi import FastAPI, APIRouter
from pathlib import Path

app = FastAPI()
api_router = APIRouter()


# @app.get("/")
@api_router.get("/", status_code=200)
async def root() -> None:
    return {"message": "Hello World"}


@api_router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8001, reload=True, access_log=False)
