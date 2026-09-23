import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import quotes

# Create tables on startup if they don't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CT Cleaning Service API")

# Allow the frontend to call the API even if served from a different origin
# during local development (e.g. opening index.html directly, or a separate
# dev server). In production, both are served from this same app anyway.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quotes.router)

# Serve the static site (index.html, css, etc.) from the project root,
# one directory up from backend/. This means running this one server gives
# you the whole website AND the API at the same origin — no CORS issues,
# and it's what gets deployed.
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")
