from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, DateTime
from app.models.base import BaseModel

class SaaSRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    IMPLEMENTATION = "IMPLEMENTATION"

class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class OnboardingTaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"

class SaaSAdmin(BaseModel):
    __tablename__ = "saas_admins"

    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(SaaSRole), nullable=False)
    is_active = Column(Boolean, default=True)
    full_name = Column(String)
    phone = Column(String)

class SupportTicket(BaseModel):
    __tablename__ = "support_tickets"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(SQLEnum(TicketStatus), nullable=False, default=TicketStatus.OPEN)
    priority = Column(SQLEnum(TicketPriority), nullable=False, default=TicketPriority.MEDIUM)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("saas_admins.id"))
    resolved_at = Column(DateTime)
    resolution_notes = Column(Text)

class TicketComment(BaseModel):
    __tablename__ = "ticket_comments"

    ticket_id = Column(Integer, ForeignKey("support_tickets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # For internal team notes

class OnboardingTask(BaseModel):
    __tablename__ = "onboarding_tasks"

    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(OnboardingTaskStatus), nullable=False, default=OnboardingTaskStatus.PENDING)
    assigned_to_id = Column(Integer, ForeignKey("saas_admins.id"))
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    completion_notes = Column(Text)
    order = Column(Integer, nullable=False)  # For task sequence
    is_blocking = Column(Boolean, default=False)  # If this task blocks other tasks