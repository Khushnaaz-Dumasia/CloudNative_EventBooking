import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Get the absolute path of the directory where THIS file (database.py) is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Combine that directory with the database filename
DB_PATH = os.path.join(BASE_DIR, "booking.db")

# 3. Use the absolute path for the SQLite connection string
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# To use Azure SQL Server later, swap the URL.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()