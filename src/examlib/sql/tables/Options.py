"""SQLAlchemy Options Module."""
from sqlalchemy import Column, Integer, ForeignKey
from .Base import Base


class Options(Base):
    """Options table."""

    __tablename__ = "options"
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True, nullable=False)
