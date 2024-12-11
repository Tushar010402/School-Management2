"""
This module contains all SQLAlchemy relationship definitions to avoid circular imports.
"""
from sqlalchemy.orm import relationship

def setup_relationships():
    from app.models.student import Student, Guardian, StudentDocument, StudentNote
    from app.models.user import User
    from app.models.tenant import Tenant
    from app.models.school import School
    from app.models.academic_core import Subject, AcademicYear, Class, Section, StudentSection, TeacherSection
    from app.models.saas import SaaSAdmin, SupportTicket, TicketComment, OnboardingTask
    from app.models.fee import FeeStructure, FeeDiscount, StudentFee, FeePayment

    # Student relationships
    Student.tenant = relationship("Tenant")
    Student.user = relationship("User")
    Student.guardians = relationship("Guardian", back_populates="student_ref", cascade="all, delete-orphan")
    Student.documents = relationship("StudentDocument", back_populates="student_ref", cascade="all, delete-orphan")
    Student.notes = relationship("StudentNote", back_populates="student_ref", cascade="all, delete-orphan")

    # Guardian relationships
    Guardian.student_ref = relationship("Student", back_populates="guardians")
    Guardian.user = relationship("User")

    # StudentDocument relationships
    StudentDocument.student_ref = relationship("Student", back_populates="documents")
    StudentDocument.uploader = relationship("User", foreign_keys=[StudentDocument.uploaded_by])
    StudentDocument.verifier = relationship("User", foreign_keys=[StudentDocument.verified_by])

    # StudentNote relationships
    StudentNote.student_ref = relationship("Student", back_populates="notes")
    StudentNote.author = relationship("User", back_populates="student_notes")

    # User relationships
    User.tenant = relationship("Tenant", back_populates="users")
    User.created_tickets = relationship("SupportTicket", back_populates="created_by", foreign_keys="[SupportTicket.created_by_id]")
    User.ticket_comments = relationship("TicketComment", back_populates="user")

    # Tenant relationships
    Tenant.schools = relationship("School", back_populates="tenant", cascade="all, delete-orphan")
    Tenant.users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")

    # School relationships
    School.tenant = relationship("Tenant", back_populates="schools")
    School.academic_years = relationship("AcademicYear", back_populates="school")
    School.classes = relationship("Class", back_populates="school")
    School.subjects = relationship("Subject", back_populates="school")

    # Academic relationships
    Subject.tenant = relationship("Tenant", back_populates="subjects")
    Subject.school = relationship("School", back_populates="subjects")
    Subject.teacher_sections = relationship("TeacherSection", back_populates="subject_ref")

    AcademicYear.tenant = relationship("Tenant", back_populates="academic_years")
    AcademicYear.school = relationship("School", back_populates="academic_years")
    AcademicYear.classes = relationship("Class", back_populates="academic_year")

    Class.tenant = relationship("Tenant", back_populates="classes")
    Class.school = relationship("School", back_populates="classes")
    Class.academic_year = relationship("AcademicYear", back_populates="classes")
    Class.sections = relationship("Section", back_populates="class_")

    Section.tenant = relationship("Tenant", back_populates="sections")
    Section.class_ = relationship("Class", back_populates="sections")
    Section.students = relationship("StudentSection", back_populates="section")
    Section.teachers = relationship("TeacherSection", back_populates="section")

    StudentSection.tenant = relationship("Tenant")
    StudentSection.student = relationship("StudentProfile")
    StudentSection.section = relationship("Section", back_populates="students")

    TeacherSection.tenant = relationship("Tenant")
    TeacherSection.teacher = relationship("User")
    TeacherSection.section = relationship("Section", back_populates="teachers")
    TeacherSection.subject_ref = relationship("Subject", back_populates="teacher_sections")

    # SaaS relationships
    SaaSAdmin.assigned_tickets = relationship("SupportTicket", back_populates="assigned_to")
    SaaSAdmin.assigned_tasks = relationship("OnboardingTask", back_populates="assigned_to")

    SupportTicket.school = relationship("School", back_populates="support_tickets")
    SupportTicket.created_by = relationship("User", back_populates="created_tickets")
    SupportTicket.assigned_to = relationship("SaaSAdmin", back_populates="assigned_tickets")
    SupportTicket.comments = relationship("TicketComment", back_populates="ticket")

    TicketComment.ticket = relationship("SupportTicket", back_populates="comments")
    TicketComment.user = relationship("User", back_populates="ticket_comments")

    OnboardingTask.school = relationship("School", back_populates="onboarding_tasks")
    OnboardingTask.assigned_to = relationship("SaaSAdmin", back_populates="assigned_tasks")
    OnboardingTask.dependencies = relationship(
        "OnboardingTask",
        secondary="task_dependencies",
        primaryjoin="OnboardingTask.id==task_dependencies.c.task_id",
        secondaryjoin="OnboardingTask.id==task_dependencies.c.depends_on_id",
        backref="dependent_tasks",
        lazy="joined"
    )

    # Fee relationships
    FeeStructure.tenant = relationship("Tenant")
    FeeStructure.school = relationship("School")
    FeeStructure.academic_year = relationship("AcademicYear")
    FeeStructure.class_ = relationship("Class")
    FeeStructure.discounts = relationship("FeeDiscount", back_populates="fee_structure", cascade="all, delete-orphan")
    FeeStructure.student_fees = relationship("StudentFee", back_populates="fee_structure", cascade="all, delete-orphan")

    FeeDiscount.tenant = relationship("Tenant")
    FeeDiscount.school = relationship("School")
    FeeDiscount.fee_structure = relationship("FeeStructure", back_populates="discounts")

    StudentFee.tenant = relationship("Tenant")
    StudentFee.student = relationship("Student")
    StudentFee.fee_structure = relationship("FeeStructure", back_populates="student_fees")
    StudentFee.discount = relationship("FeeDiscount")
    StudentFee.payments = relationship("FeePayment", back_populates="student_fee", cascade="all, delete-orphan")

    FeePayment.tenant = relationship("Tenant")
    FeePayment.student_fee = relationship("StudentFee", back_populates="payments")