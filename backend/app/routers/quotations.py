from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func

from .. import models, schemas
from ..database import get_db
from ..auth import require_admin
from ..pdf_utils import generate_quotation_pdf

router = APIRouter(prefix="/api/quotations", tags=["quotations"], dependencies=[Depends(require_admin)])


def _next_quotation_number(db: Session) -> str:
    count = db.query(func.count(models.Quotation.id)).scalar() or 0
    return f"CTQ-{count + 1:04d}"


@router.post("", response_model=schemas.QuotationOut, status_code=201)
def create_quotation(payload: schemas.QuotationCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    items_data = data.pop("items")

    quotation = models.Quotation(quotation_number=_next_quotation_number(db), **data)
    db.add(quotation)
    db.flush()  # get quotation.id before adding items

    for item in items_data:
        db.add(models.QuotationItem(quotation_id=quotation.id, **item))

    db.commit()
    db.refresh(quotation)
    return quotation


@router.get("", response_model=List[schemas.QuotationOut])
def list_quotations(db: Session = Depends(get_db)):
    return (
        db.query(models.Quotation)
        .options(joinedload(models.Quotation.items))
        .order_by(desc(models.Quotation.created_at))
        .all()
    )


@router.get("/{quotation_id}", response_model=schemas.QuotationOut)
def get_quotation(quotation_id: int, db: Session = Depends(get_db)):
    quotation = (
        db.query(models.Quotation)
        .options(joinedload(models.Quotation.items))
        .filter(models.Quotation.id == quotation_id)
        .first()
    )
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation


@router.get("/{quotation_id}/pdf")
def download_quotation_pdf(quotation_id: int, db: Session = Depends(get_db)):
    quotation = (
        db.query(models.Quotation)
        .options(joinedload(models.Quotation.items))
        .filter(models.Quotation.id == quotation_id)
        .first()
    )
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    pdf_bytes = generate_quotation_pdf(quotation)
    filename = f"{quotation.quotation_number}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
