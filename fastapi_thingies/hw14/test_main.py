from fastapi.testclient import TestClient
from main import app, logger
import os

client = TestClient(app)

def test_send_email_endpoint():
    response = client.post("/send-email", json={
        "user_email": "test@example.com",
        "user_name": "TestUser",
        "subject": "Hello",
        "message": "This is a test email"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "request for sending mail was accepted"}

def test_log_written_on_email_send():
    if os.path.exists("user_actions.log"):
        os.remove("user_actions.log")

    client.post("/send-email", json={
        "user_email": "test@example.com",
        "user_name": "TestUser",
        "subject": "Hello",
        "message": "This is a test email"
    })

    import time
    time.sleep(3)

    with open("user_actions.log", "r") as f:
        logs = f.read()
        assert "User: TestUser | Action: send_email" in logs
        assert "Email sent to test@example.com" in logs
