from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Order(BaseModel):
    product_name: str = Field(..., min_length=1, description="Назва продукту не може бути порожньою")
    quantity: int = Field(default=1, gt=0, description="Кількість має бути більше нуля")
    price_per_unit: float = Field(..., gt=0, description="Ціна має бути позитивною")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class User(BaseModel):
    name: str
    email: EmailStr
    orders: List[Order] = []

users_db: dict[str, User] = {}

@app.post("/users/", response_model=User)
def create_user(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Користувач з такою електронною поштою вже існує")
    users_db[user.email] = user
    return user

@app.get("/users/", response_model=User)
def get_user_by_email(email: EmailStr = Query(..., description="Введіть дійсну електронну пошту")):
    user = users_db.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return user
