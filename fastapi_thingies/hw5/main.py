from fastapi import FastAPI, Path, Query, Header, HTTPException
from datetime import datetime
from typing import Optional

app = FastAPI()

@app.get("/user/{user_id}")
def get_user_info(
    user_id: int = Path(..., description="User ID must be an integer"),
    timestamp: Optional[str] = Query(None, description="Optional timestamp in ISO format"),
    x_client_version: str = Header(..., convert_underscores=False)
):
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()

    return {
        "user_id": user_id,
        "timestamp": timestamp,
        "X-Client-Version": x_client_version,
        "message": f"Hello, user {user_id}!"
    }
