import pytest
from fastapi.testclient import TestClient
from main import app
from io import BytesIO

client = TestClient(app)

def create_test_image(format="JPEG"):
    from PIL import Image
    img = Image.new("RGB", (100, 100), color=(73, 109, 137))
    buf = BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    return buf

def test_upload_valid_image():
    img = create_test_image()
    files = {"files": ("test.jpg", img, "image/jpeg")}
    response = client.post("/upload/", files=files)
    assert response.status_code == 200
    json_resp = response.json()
    assert "uploaded_files" in json_resp
    assert json_resp["uploaded_files"][0]["original_filename"] == "test.jpg"

def test_upload_invalid_extension():
    img = create_test_image()
    files = {"files": ("test.gif", img, "image/gif")}
    response = client.post("/upload/", files=files)
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"]

def test_upload_too_large_file():
    big_file = BytesIO(b"x" * (6 * 1024 * 1024))  # 6 MB
    files = {"files": ("big.jpg", big_file, "image/jpeg")}
    response = client.post("/upload/", files=files)
    assert response.status_code == 400
    assert "too large" in response.json()["detail"]
