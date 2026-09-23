from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from .. import models, schemas
from ..database import get_db
from ..auth import require_admin

router = APIRouter(prefix="/api/quotes", tags=["quotes"])


@router.post("", response_model=schemas.QuoteRequestOut, status_code=201)
def create_quote_request(payload: schemas.QuoteRequestCreate, db: Session = Depends(get_db)):
    """Public endpoint — the website's quote form submits here. No auth required."""
    lead = models.QuoteRequest(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("", response_model=List[schemas.QuoteRequestOut], dependencies=[Depends(require_admin)])
def list_quote_requests(db: Session = Depends(get_db)):
    """Admin-only — lists leads, newest first."""
    return db.query(models.QuoteRequest).order_by(desc(models.QuoteRequest.created_at)).all()


@router.patch("/{quote_id}", response_model=schemas.QuoteRequestOut, dependencies=[Depends(require_admin)])
def update_quote_status(quote_id: int, payload: schemas.QuoteStatusUpdate, db: Session = Depends(get_db)):
    """Admin-only — update a lead's status (new/contacted/won/lost)."""
    lead = db.query(models.QuoteRequest).filter(models.QuoteRequest.id == quote_id).first()
    if not lead:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Quote request not found")
    lead.status = payload.status
    db.commit()
    db.refresh(lead)
    return lead
