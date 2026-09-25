from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from .models import LeadStatus, ServiceType


class QuoteRequestCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    service_type: ServiceType
    org_name: Optional[str] = None
    location: str
    date_needed: Optional[date] = None
    notes: Optional[str] = None


class QuoteRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    email: Optional[str] = None
    service_type: ServiceType
    org_name: Optional[str] = None
    location: str
    date_needed: Optional[date] = None
    notes: Optional[str] = None
    status: LeadStatus
    created_at: datetime


class QuoteStatusUpdate(BaseModel):
    status: LeadStatus


# --- Quotations ---

class QuotationItemCreate(BaseModel):
    description: str
    quantity: float = 1
    unit_price: float = 0


class QuotationItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    quantity: float
    unit_price: float


class QuotationCreate(BaseModel):
    client_name: str
    client_phone: str
    client_email: Optional[str] = None
    client_org: Optional[str] = None
    client_location: str
    valid_until: Optional[date] = None
    notes: Optional[str] = None
    items: List[QuotationItemCreate]


class QuotationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quotation_number: str
    client_name: str
    client_phone: str
    client_email: Optional[str] = None
    client_org: Optional[str] = None
    client_location: str
    date_issued: date
    valid_until: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime
    items: List[QuotationItemOut]
