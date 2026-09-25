import enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Date, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
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


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    quotation_number = Column(String(30), unique=True, nullable=False)
    client_name = Column(String(120), nullable=False)
    client_phone = Column(String(40), nullable=False)
    client_email = Column(String(160), nullable=True)
    client_org = Column(String(160), nullable=True)
    client_location = Column(String(200), nullable=False)
    date_issued = Column(Date, default=date.today)
    valid_until = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete-orphan")


class QuotationItem(Base):
    __tablename__ = "quotation_items"

    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False)
    description = Column(String(300), nullable=False)
    quantity = Column(Float, nullable=False, default=1)
    unit_price = Column(Float, nullable=False, default=0)

    quotation = relationship("Quotation", back_populates="items")
