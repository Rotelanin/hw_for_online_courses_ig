from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from datetime import datetime
import time

app = FastAPI()


@app.middleware("http")
async def log_and_check_header(request: Request, call_next):
    method = request.method
    url = str(request.url)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Запит: {method} {url}")

    if "X-Custom-Header" not in request.headers:
        return JSONResponse(
            status_code=400,
            content={"detail": "Заголовок 'X-Custom-Header' є обов’язковим."}
        )

    response = await call_next(request)
    return response

@app.get("/hello", tags=["Тестові"], summary="Привітання")
def say_hello():
    """
    Тестовий маршрут, який повертає привітання.
    """
    return {"message": "Привіт від FastAPI!"}

@app.post("/echo", tags=["Тестові"], summary="Повторення повідомлення")
def echo_data(data: dict):
    """
    Повертає те саме, що отримано в запиті.
    """
    return {"echo": data}

@app.get("/header", tags=["Тестові"], summary="Показати заголовок")
def show_custom_header(request: Request):
    """
    Повертає значення заголовка `X-Custom-Header`.
    """
    header_value = request.headers.get("X-Custom-Header")
    return {"X-Custom-Header": header_value}
