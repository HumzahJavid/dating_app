from pathlib import Path

from fastapi import APIRouter, Body, Request, status
from fastapi.templating import Jinja2Templates

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_PATH / "templates")

router = APIRouter()


def create_chat_session_id(id1, id2):
    id_list = [id1, id2]
    id_list.sort()
    return id_list[0] + "-" + id_list[1]


@router.get("/chat", status_code=200)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.post("/initiate_chat", status_code=status.HTTP_201_CREATED)
async def initiate_chat(user_initiating_id=Body(...), user_receiving_id=Body(...)):
    print("initiating chat?")
    chat_session_id = create_chat_session_id(user_initiating_id, user_receiving_id)
    print("returning", chat_session_id)
    return chat_session_id
