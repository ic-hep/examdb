"""SQLAlchemy Marks Module."""
from sqlalchemy import Column, Integer, ForeignKey
from .Base import Base


class Marks(Base):
    """Marks table."""

    __tablename__ = "marks"
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True, nullable=False)
    result = Column(Integer, nullable=False)
