import logging
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
from pydantic import BaseModel, EmailStr
import aiofiles
from PIL import Image
import io
import os
from typing import Optional

app = FastAPI()
UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

logger = logging.getLogger("user_actions")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("user_actions.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class EmailRequest(BaseModel):
    user_email: EmailStr
    user_name: str
    subject: str
    message: str

async def fake_send_email(user_email: str, subject: str, message: str):
    """
    imitation of sending mail cuz I do not have any official stuff I think-
    """
    import asyncio
    await asyncio.sleep(2)
    logger.info(f"Email sent to {user_email} with subject '{subject}'")

def log_user_action(user_name: str, action: str, details: Optional[str] = None):
    log_msg = f"User: {user_name} | Action: {action}"
    if details:
        log_msg += f" | Details: {details}"
    logger.info(log_msg)

@app.post("/send-email")
async def send_email(data: EmailRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(fake_send_email, data.user_email, data.subject, data.message)
    log_user_action(data.user_name, "send_email", f"To: {data.user_email}, Subject: {data.subject}")
    return {"message": "request for sending mail was accepted"}

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def resize_image(input_path: str, output_path: str, size=(800, 600)):
    """image size change"""
    with Image.open(input_path) as img:
        img = img.resize(size)
        img.save(output_path)

async def save_upload_file(upload_file: UploadFile, destination: str):
    async with aiofiles.open(destination, "wb") as out_file:
        content = await upload_file.read()
        await out_file.write(content)

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images are supported")
    
    upload_path = os.path.join(UPLOAD_DIR, file.filename)
    processed_path = os.path.join(PROCESSED_DIR, file.filename)

    await save_upload_file(file, upload_path)

    background_tasks.add_task(resize_image, upload_path, processed_path)

    log_user_action("anonymous", "upload_file", f"File: {file.filename}")

    return {"message": f"file {file.filename} is in query"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
