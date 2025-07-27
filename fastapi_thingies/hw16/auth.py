from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models import User

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "alice": {"username": "alice"},
    "bob": {"username": "bob"},
}

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in fake_users_db:
            raise HTTPException(status_code=401)
        return User(username=username)
    except JWTError:
        raise HTTPException(status_code=401)
