import os
import shutil
import uuid

from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO

app = FastAPI()

ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png"}
MAX_FILE_SIZE_MB = 5
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

def validate_file(file: UploadFile):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type {ext} not allowed")

async def save_file_to_disk(file: UploadFile, filename: str):
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

def optimize_image(path: str):
    with Image.open(path) as img:
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        else:
            img = img.convert("RGB")
        max_size = (1024, 1024)
        img.thumbnail(max_size)
        img.save(path, "JPEG", quality=85)

@app.post("/upload/")
async def upload_images(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    saved_files = []

    for file in files:
        validate_file(file)
        contents = await file.read()
        size_mb = len(contents) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(status_code=400, detail=f"File {file.filename} too large (>5MB)")
        await file.seek(0)
        unique_filename = f"{uuid.uuid4().hex}.jpg"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        await save_file_to_disk(file, file_path)
        background_tasks.add_task(optimize_image, file_path)
        saved_files.append({"original_filename": file.filename, "saved_as": unique_filename})
    return JSONResponse({"uploaded_files": saved_files})
