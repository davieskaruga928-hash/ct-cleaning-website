# CT Cleaning Service — Website

A website built for CT Cleaning Service, a Nairobi-based cleaning company serving homes, offices, churches/events, and large institutions (e.g. Northlands), to generate more client leads and present a more credible, institutional-grade brand.

## Status

**Phase 1: static marketing site — done**
- [x] Homepage
- [x] Services page
- [x] About page
- [x] Gallery page (placeholder photos, to be replaced)
- [x] Contact page
- [x] Quote request page

**Phase 2: backend — done**
- [x] FastAPI + SQLAlchemy backend, quote form saves real leads to a database
- [x] Admin dashboard (`admin.html`) for viewing and updating lead status
- [ ] Real content, photos, and contact details (currently placeholders)
- [ ] Deployment to a live domain

## Tech stack

- Frontend: HTML / CSS (vanilla). Fonts: Archivo (headings), Inter (body).
- Backend: FastAPI + SQLAlchemy, SQLite by default (switchable to PostgreSQL)
- Admin auth: simple shared password via request header

## Project structure

```
ct-cleaning-website/
├── index.html, services.html, about.html, contact.html, quote.html, gallery.html
├── admin.html                 # password-protected lead dashboard
├── css/
│   └── style.css
├── assets/
└── backend/
    ├── requirements.txt
    ├── .env.example
    └── app/
        ├── main.py             # FastAPI app, serves API + static site
        ├── database.py
        ├── models.py
        ├── schemas.py
        ├── auth.py
        └── routers/
            └── quotes.py
```

## Running locally

1. `cd backend`
2. `python -m venv venv` then activate it (`venv\Scripts\activate` on Windows, `source venv/bin/activate` on Mac/Linux)
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set a real `ADMIN_PASSWORD`
5. `uvicorn app.main:app --reload`
6. Open `http://127.0.0.1:8000` — this serves the whole site AND the API from one server (no separate frontend server needed)
7. Admin dashboard: `http://127.0.0.1:8000/admin.html`

By default this uses a local SQLite file (`quotes.db`, auto-created, git-ignored). To use PostgreSQL instead, set `DATABASE_URL` in `.env`.

## Notes

Content (stats, contact details, photos) is currently placeholder and will be swapped for real business details.

