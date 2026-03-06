from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, database
from database import engine, SessionLocal

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development only; narrow this down for production
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


class EventCreate(BaseModel):
    title: str
    location: str
    date_time: str

class EventResponse(EventCreate):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Event Service Running"}

@app.post("/events", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    new_event = models.Event(title=event.title, location=event.location, date_time=event.date_time)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@app.get("/events", response_model=list[EventResponse])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Event).offset(skip).limit(limit).all()

# CRITICAL: This endpoint allows the Booking Service to verify an event exists
@app.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event