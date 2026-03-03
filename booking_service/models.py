from sqlalchemy import Column, Integer
from database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)   # In a microservice, this references the User Service
    event_id = Column(Integer, index=True)  # In a microservice, this references the Event Service
