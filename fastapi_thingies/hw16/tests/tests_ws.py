import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

@pytest.mark.asyncio
async def test_websocket_chat():
    response = client.post("/token", params={"username": "bob"})
    token = response.json()["access_token"]

    with client.websocket_connect(f"/ws?token={token}") as websocket:
        websocket.send_text("Hello <script>alert('XSS')</script>")
        data = websocket.receive_text()
        assert "&lt;script&gt;" in data
