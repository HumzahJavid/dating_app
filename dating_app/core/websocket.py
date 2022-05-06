from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from dating_app.core.ConnectionManager import ConnectionManager

router = APIRouter()

manager = ConnectionManager()


@router.websocket("/ws/{chat_session_id}")
async def websocket_endpoint(websocket: WebSocket, chat_session_id: str):
    await manager.connect(websocket)
    sender = chat_session_id.split("-")[0]
    response = {"sender": sender, "message": "started chat"}
    await manager.broadcast(response)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"data server side is {data}")
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        response["message"] = "left"
        await manager.broadcast(response)
