from datetime import datetime, date
from typing import Optional
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
