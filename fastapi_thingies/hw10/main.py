from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from hashlib import sha256
import secrets

app = FastAPI()

users_db = {
    "user1": {
        "username": "user1",
        "password": sha256("password123".encode()).hexdigest(),
        "full_name": "Іван Іванович"
    },
    "admin": {
        "username": "admin",
        "password": sha256("adminpass".encode()).hexdigest(),
        "full_name": "Адміністратор Системи"
    }
}

basic_auth = HTTPBasic()

def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(basic_auth)):
    user = users_db.get(credentials.username)
    password_hash = sha256(credentials.password.encode()).hexdigest()
    if not user or not secrets.compare_digest(user["password"], password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірні облікові дані",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

@app.get("/basic-protected")
def basic_protected_route(user: dict = Depends(verify_basic_auth)):
    return {"message": f"Привіт, {user['full_name']}! Ви увійшли через Basic Auth."}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    password_hash = sha256(form_data.password.encode()).hexdigest()
    if not user or not secrets.compare_digest(user["password"], password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірне ім’я користувача або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = f"token-{user['username']}"
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = token.replace("token-", "")
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="Неправильний токен")
    return user

@app.get("/oauth2-protected")
def oauth2_protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Привіт, {current_user['full_name']}! Ви увійшли через OAuth2."}
