"""
Fee management models.
"""
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum as SQLEnum, Text, Date
from app.models.base import BaseModel

class FeeType(str, Enum):
    TUITION = "TUITION"
    ADMISSION = "ADMISSION"
    EXAM = "EXAM"
    TRANSPORT = "TRANSPORT"
    LIBRARY = "LIBRARY"
    LABORATORY = "LABORATORY"
    SPORTS = "SPORTS"
    UNIFORM = "UNIFORM"
    BOOKS = "BOOKS"
    MISCELLANEOUS = "MISCELLANEOUS"

class PaymentInterval(str, Enum):
    ONCE = "ONCE"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    HALF_YEARLY = "HALF_YEARLY"
    YEARLY = "YEARLY"

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PARTIAL = "PARTIAL"
    PAID = "PAID"
    OVERDUE = "OVERDUE"

class FeeStructure(BaseModel):
    __tablename__ = "fee_structures"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    
    name = Column(String, nullable=False)
    fee_type = Column(SQLEnum(FeeType), nullable=False)
    amount = Column(Float, nullable=False)
    payment_interval = Column(SQLEnum(PaymentInterval), nullable=False)
    description = Column(Text)
    is_optional = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

class FeeDiscount(BaseModel):
    __tablename__ = "fee_discounts"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    
    name = Column(String, nullable=False)
    discount_type = Column(String, nullable=False)  # PERCENTAGE or FIXED
    discount_value = Column(Float, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

class StudentFee(BaseModel):
    __tablename__ = "student_fees"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    discount_id = Column(Integer, ForeignKey("fee_discounts.id"))
    
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    paid_amount = Column(Float, default=0)
    balance = Column(Float, nullable=False)
    status = Column(SQLEnum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    last_payment_date = Column(Date)
    notes = Column(Text)

class FeePayment(BaseModel):
    __tablename__ = "fee_payments"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    student_fee_id = Column(Integer, ForeignKey("student_fees.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String, nullable=False)  # CASH, BANK_TRANSFER, CARD, etc.
    transaction_id = Column(String)
    receipt_number = Column(String)
    notes = Column(Text)
    is_cancelled = Column(Boolean, default=False)
    cancellation_reason = Column(Text)