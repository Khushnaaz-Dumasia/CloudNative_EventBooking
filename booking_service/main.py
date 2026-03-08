from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, database
from database import engine, SessionLocal
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

import os

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8001") + "/users"
EVENT_SERVICE_URL = os.getenv("EVENT_SERVICE_URL", "http://localhost:8002") + "/events"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development only; narrow this down for production
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)



class BookingCreate(BaseModel):
    user_id: int
    event_id: int

class BookingResponse(BookingCreate):
    id: int

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():    
    return {"message": "Booking Service Running"}

@app.post("/bookings", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    # 1. VALIDATE USER: Check if the user exists in User Service
    try:
        user_resp = requests.get(f"{USER_SERVICE_URL}/{booking.user_id}", timeout=2)
        if user_resp.status_code != 200:
            raise HTTPException(
                status_code=404, 
                detail=f"User with ID {booking.user_id} not found in User Service."
            )
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to User Service at {USER_SERVICE_URL}: {e}")
        raise HTTPException(
            status_code=503, 
            detail=f"User Service is unavailable. Error: {str(e)}"
        )

    # 2. VALIDATE EVENT: Check if the event exists in Event Service
    try:
        event_resp = requests.get(f"{EVENT_SERVICE_URL}/{booking.event_id}", timeout=2)
        if event_resp.status_code != 200:
            raise HTTPException(
                status_code=404, 
                detail=f"Event with ID {booking.event_id} not found in Event Service."
            )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503, 
            detail="Event Service is unavailable. Cannot verify event."
        )

    # 3. CREATE BOOKING: Only if both above passed
    new_booking = models.Booking(user_id=booking.user_id, event_id=booking.event_id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.get("/bookings", response_model=list[BookingResponse])
def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).offset(skip).limit(limit).all()
    return bookings

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
    return {"message": "Booking deleted successfully"}