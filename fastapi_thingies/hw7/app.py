from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from datetime import datetime, date
import re

app = FastAPI()

books = []
users = []
events = []

class Book(BaseModel):
    id: int
    title: str = Field(...)
    author: str = Field(...)
    publication_year: int
    quantity: int

@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.post("/books", status_code=201)
def add_book(book: Book):
    if any(b.id == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book with this ID already exists.")
    books.append(book)
    return book

@app.get("/books/{id}", response_model=Book)
def get_book_by_id(id: int = Path(..., gt=0)):
    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found.")

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str

    @validator("first_name", "last_name")
    def name_must_be_letters(cls, v):
        if len(v) < 2 or not v.isalpha():
            raise ValueError("Must be at least 2 letters and only letters")
        return v

    @validator("password")
    def strong_password(cls, v):
        if (len(v) < 8 or
            not re.search(r"[A-Z]", v) or
            not re.search(r"[a-z]", v) or
            not re.search(r"[0-9]", v) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v)):
            raise ValueError("Password must be strong.")
        return v

    @validator("phone")
    def phone_pattern(cls, v):
        if not re.fullmatch(r"\+?\d{10,15}", v):
            raise ValueError("Invalid phone number.")
        return v

@app.post("/register", status_code=201)
def register_user(user: User):
    users.append(user)
    return {"message": "User registered successfully."}

class Event(BaseModel):
    id: int
    name: str
    description: str
    date: date
    creator: str

@app.post("/events", status_code=201)
def create_event(event: Event):
    if event.date < date.today():
        raise HTTPException(status_code=400, detail="Event date cannot be in the past.")
    events.append(event)
    return event

@app.get("/events")
def get_all_events():
    if not events:
        return Response(status_code=204)
    return events

@app.get("/events/{id}")
def get_event(id: int):
    for e in events:
        if e.id == id:
            return e
    raise HTTPException(status_code=404, detail="Event not found.")

@app.put("/events/{id}")
def update_event(id: int, updated: Event):
    for i, e in enumerate(events):
        if e.id == id:
            if updated.date < date.today():
                raise HTTPException(status_code=400, detail="Invalid event date.")
            events[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Event not found.")

@app.delete("/events/{id}")
def delete_event(id: int):
    for i, e in enumerate(events):
        if e.id == id:
            del events[i]
            return {"message": "Event deleted."}
    raise HTTPException(status_code=404, detail="Event not found.")

@app.patch("/events/{id}/reschedule")
def reschedule_event(id: int, new_date: date):
    for event in events:
        if event.id == id:
            if new_date < date.today():
                raise HTTPException(status_code=400, detail="Invalid new date.")
            event.date = new_date
            return event
    raise HTTPException(status_code=404, detail="Event not found.")

rsvps = {}

@app.post("/events/{id}/rsvp")
def rsvp_event(id: int, email: EmailStr):
    for e in events:
        if e.id == id:
            rsvps.setdefault(id, set())
            if email in rsvps[id]:
                raise HTTPException(status_code=409, detail="Already registered.")
            rsvps[id].add(email)
            return {"message": "RSVP successful."}
    raise HTTPException(status_code=404, detail="Event not found.")
