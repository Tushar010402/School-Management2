from enum import Enum
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, UniqueConstraint, Text, Float
from app.models.base import BaseModel

class WeekDay(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class GradingSystem(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    GRADE = "GRADE"
    GPA = "GPA"

class AssessmentType(str, Enum):
    EXAM = "EXAM"
    TEST = "TEST"
    QUIZ = "QUIZ"
    ASSIGNMENT = "ASSIGNMENT"
    PROJECT = "PROJECT"
    PRESENTATION = "PRESENTATION"
    PRACTICAL = "PRACTICAL"
    OTHER = "OTHER"

class Subject(BaseModel):
    __tablename__ = "subjects"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    description = Column(Text)
    credits = Column(Float)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('tenant_id', 'code', name='uq_subject_code'),
    )

class AcademicYear(BaseModel):
    __tablename__ = "academic_years"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('tenant_id', 'name', name='uq_academic_year_name'),
    )

class Class(BaseModel):
    __tablename__ = "classes"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    name = Column(String, nullable=False)
    grade_level = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('tenant_id', 'academic_year_id', 'name', name='uq_class_name'),
    )

class Section(BaseModel):
    __tablename__ = "sections"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('tenant_id', 'class_id', 'name', name='uq_section_name'),
    )

class StudentSection(BaseModel):
    __tablename__ = "student_sections"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    roll_number = Column(String)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('tenant_id', 'student_id', 'section_id', name='uq_student_section'),
    )

class TeacherSection(BaseModel):
    __tablename__ = "teacher_sections"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    is_class_teacher = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('tenant_id', 'teacher_id', 'section_id', 'subject_id', 
                        name='uq_teacher_section_subject'),
    )