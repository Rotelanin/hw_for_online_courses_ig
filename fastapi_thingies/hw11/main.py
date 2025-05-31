from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="Movie Collection API",
    description="API для керування колекцією фільмів",
    version="1.0.0",
)

class Movie(BaseModel):
    id: int = Field(..., example=1, description="Унікальний ідентифікатор фільму")
    title: str = Field(..., example="Inception", description="Назва фільму")
    director: str = Field(..., example="Christopher Nolan", description="Режисер фільму")
    release_year: int = Field(..., example=2010, ge=1888, description="Рік випуску фільму")
    rating: float = Field(..., example=8.8, ge=0.0, le=10.0, description="Рейтинг фільму")

movies_db: List[Movie] = []

@app.get("/movies", response_model=List[Movie], tags=["Movies"], summary="Отримати всі фільми", description="Цей маршрут повертає список усіх фільмів, наявних у колекції.")
def get_movies():
    """
    Повертає всі фільми з колекції.
    """
    return movies_db

@app.post("/movies", response_model=Movie, tags=["Movies"], summary="Додати новий фільм", description="Додає новий фільм у колекцію фільмів.")
def add_movie(movie: Movie):
    """
    Додає новий фільм до бази.
    Перевіряє, чи унікальний `id`.
    """
    for existing_movie in movies_db:
        if existing_movie.id == movie.id:
            raise HTTPException(status_code=400, detail="Фільм з таким ID вже існує.")
    movies_db.append(movie)
    return movie

@app.get("/movies/{movie_id}", response_model=Movie, tags=["Movies"], summary="Отримати фільм за ID", description="Повертає фільм з бази даних за вказаним ID.")
def get_movie(movie_id: int = Path(..., description="ID фільму, який ви хочете отримати", ge=1)):
    """
    Отримує один фільм за його `id`.
    """
    for movie in movies_db:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Фільм не знайдено.")

@app.delete("/movies/{movie_id}", tags=["Movies"], summary="Видалити фільм за ID", description="Видаляє фільм з бази даних за вказаним ID.")
def delete_movie(movie_id: int = Path(..., description="ID фільму, який ви хочете видалити", ge=1)):
    """
    Видаляє фільм за його `id`.
    """
    for i, movie in enumerate(movies_db):
        if movie.id == movie_id:
            del movies_db[i]
            return {"detail": "Фільм успішно видалено"}
    raise HTTPException(status_code=404, detail="Фільм не знайдено.")
