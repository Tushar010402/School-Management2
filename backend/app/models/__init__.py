from app.models.base import BaseModel
from app.models.tenant import Tenant
from app.models.school import School
from app.models.user import User
from app.models.enums import UserRole
from app.models.student import Student, Guardian, StudentDocument, StudentNote
from app.models.academic_core import Subject, AcademicYear, Class, Section, StudentSection, TeacherSection
from app.models.saas import SaaSAdmin, SupportTicket, TicketComment, OnboardingTask
from app.models.fee import FeeStructure, FeeDiscount, StudentFee, FeePayment, FeeType, PaymentInterval, PaymentStatus
from app.models.relationships import setup_relationships

__all__ = [
    "BaseModel",
    "Tenant",
    "School",
    "User",
    "UserRole",
    "Student",
    "Guardian",
    "StudentDocument",
    "StudentNote",
    "Subject",
    "AcademicYear",
    "Class",
    "Section",
    "StudentSection",
    "TeacherSection",
    "SaaSAdmin",
    "SupportTicket",
    "TicketComment",
    "OnboardingTask",
    "FeeStructure",
    "FeeDiscount",
    "StudentFee",
    "FeePayment",
    "FeeType",
    "PaymentInterval",
    "PaymentStatus"
]

# Set up all model relationships
setup_relationships()