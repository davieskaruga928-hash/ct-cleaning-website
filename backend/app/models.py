import enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Enum as SAEnum
from .database import Base


class LeadStatus(str, enum.Enum):
    new = "new"
    contacted = "contacted"
    won = "won"
    lost = "lost"


class ServiceType(str, enum.Enum):
    institutional = "institutional"
    office = "office"
    church_event = "church-event"
    home = "home"
    other = "other"


class QuoteRequest(Base):
    __tablename__ = "quote_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(40), nullable=False)
    email = Column(String(160), nullable=True)
    service_type = Column(SAEnum(ServiceType), nullable=False)
    org_name = Column(String(160), nullable=True)
    location = Column(String(200), nullable=False)
    date_needed = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(SAEnum(LeadStatus), nullable=False, default=LeadStatus.new)
    created_at = Column(DateTime, default=datetime.utcnow)
