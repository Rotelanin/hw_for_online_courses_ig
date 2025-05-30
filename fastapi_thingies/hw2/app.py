from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

names = []

class NameRequest(BaseModel):
    name: str

@app.post("/add-name")
def add_name(request: NameRequest):
    if request.name in names:
        raise HTTPException(status_code=400, detail="Ім'я вже існує")
    names.append(request.name)
    return {"message": f"Ім'я '{request.name}' додано успішно."}

@app.get("/list-names")
def list_names():
    return {"names": names}

@app.delete("/delete-name")
def delete_name(request: NameRequest):
    if request.name not in names:
        raise HTTPException(status_code=404, detail="Ім'я не знайдено")
    names.remove(request.name)
    return {"message": f"Ім'я '{request.name}' успішно видалено."}

# uvicorn main:app --reload
