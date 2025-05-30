from fastapi import FastAPI, HTTPException
import aiohttp
import aiomysql
import asyncio

app = FastAPI()

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "youruser",
    "password": "yourpassword",
    "db": "yourdb"
}


@app.get("/external-users")
async def get_external_users():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://jsonplaceholder.typicode.com/users") as response:
            if response.status != 200:
                raise HTTPException(status_code=500, detail="Не вдалося отримати користувачів")
            return await response.json()


async def get_db_connection():
    return await aiomysql.connect(**DB_CONFIG)

@app.get("/db-users")
async def get_db_users():
    conn = await get_db_connection()
    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute("SELECT * FROM users")
        users = await cur.fetchall()
    conn.close()
    return users

@app.post("/db-users")
async def add_user(name: str, email: str):
    conn = await get_db_connection()
    async with conn.cursor() as cur:
        await cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        await conn.commit()
    conn.close()
    return {"message": "Користувач доданий"}

@app.delete("/db-users/{user_id}")
async def delete_user(user_id: int):
    conn = await get_db_connection()
    async with conn.cursor() as cur:
        await cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        await conn.commit()
    conn.close()
    return {"message": f"Користувача з ID {user_id} видалено"}
