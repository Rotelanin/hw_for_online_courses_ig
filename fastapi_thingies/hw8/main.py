from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    director: str = Field(..., min_length=1)
    release_year: int = Field(..., ge=1888)
    rating: float = Field(..., ge=0.0, le=10.0)

    @validator('release_year')
    def check_release_year(cls, value):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError("Рік випуску не може бути у майбутньому")
        return value

movies_db: List[Movie] = []

@app.get("/movies", response_model=List[Movie])
def get_movies():
    return movies_db

@app.post("/movies", response_model=Movie)
def add_movie(movie: Movie):
    if any(existing.id == movie.id for existing in movies_db):
        raise HTTPException(status_code=400, detail="Фільм з таким ID вже існує")
    movies_db.append(movie)
    return movie

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies_db:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Фільм не знайдено")

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for i, movie in enumerate(movies_db):
        if movie.id == movie_id:
            del movies_db[i]
            return {"detail": "Фільм успішно видалено"}
    raise HTTPException(status_code=404, detail="Фільм не знайдено")
