import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Local dev default: SQLite file, zero setup required.
# For production (or to match the Shepherd stack), set DATABASE_URL, e.g.:
#   postgresql://user:password@localhost:5432/ct_cleaning
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quotes.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
