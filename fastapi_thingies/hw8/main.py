from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    director: str = Field(..., min_length=1)
    release_year: int
    rating: float = Field(..., ge=0, le=10)

    @validator("release_year")
    def check_release_year(cls, v):
        current_year = datetime.now().year
        if v > current_year:
            raise ValueError(f"Release year cannot be in the future ({current_year})")
        return v

movies_db: List[Movie] = []

@app.get("/movies", response_model=List[Movie])
def get_all_movies():
    return movies_db

@app.post("/movies", response_model=Movie)
def add_movie(movie: Movie):
    if any(m.id == movie.id for m in movies_db):
        raise HTTPException(status_code=400, detail="Movie with this ID already exists.")
    movies_db.append(movie)
    return movie

@app.get("/movies/{id}", response_model=Movie)
def get_movie_by_id(id: int = Path(..., gt=0)):
    for movie in movies_db:
        if movie.id == id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found.")

@app.delete("/movies/{id}")
def delete_movie(id: int = Path(..., gt=0)):
    for index, movie in enumerate(movies_db):
        if movie.id == id:
            del movies_db[index]
            return {"message": f"Movie with ID {id} deleted."}
    raise HTTPException(status_code=404, detail="Movie not found.")
