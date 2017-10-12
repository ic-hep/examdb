"""SQLAlchemy Course Aliases Module."""
from sqlalchemy import Column, Integer, String, ForeignKey
from .Base import Base


class CourseAliases(Base):
    """Course aliases table."""

    __tablename__ = "course_aliases"
    name = Column(String(10), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
