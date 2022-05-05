from pathlib import Path

from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates

from dating_app.schemas.ChatModel import InitiateChat, InitiateChatResponse

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_PATH / "templates")

router = APIRouter()


def create_chat_session_id(fields: InitiateChat):
    id_list = [fields.user_initiating_id, fields.user_receiving_id]
    id_list.sort()
    return id_list[0] + "-" + id_list[1]


@router.get("/chat", status_code=200)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.post(
    "/initiate_chat",
    status_code=status.HTTP_201_CREATED,
    response_model=InitiateChatResponse,
)
async def initiate_chat(fields: InitiateChat):
    print("initiating chat?")
    print(fields)
    chat_session_id = create_chat_session_id(fields)
    return InitiateChatResponse(chat_session_id=chat_session_id)
