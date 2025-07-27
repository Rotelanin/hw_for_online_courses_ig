from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from auth import get_current_user, create_token, fake_users_db
from manager import ConnectionManager
from utils import sanitize_message
from models import User
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

@app.post("/token")
async def login(username: str):
    if username not in fake_users_db:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"access_token": create_token({"sub": username}), "token_type": "bearer"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    user = await get_current_user(token)
    await manager.connect(websocket, user.username)
    try:
        while True:
            data = await websocket.receive_text()
            clean_msg = sanitize_message(data)
            await manager.broadcast(f"{user.username}: {clean_msg}")
    except WebSocketDisconnect:
        manager.disconnect(user.username)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")
