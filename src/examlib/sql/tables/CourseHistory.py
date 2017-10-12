"""SQLAlchemy Course History Module."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .Base import Base


class CourseHistory(Base):
    """Course history table."""

    __tablename__ = "course_history"
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True, nullable=False)
    year = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(30))
    mean = Column(Float, nullable=False)
    twosigma = Column(Float, nullable=False)
    num = Column(Integer, nullable=False)
    var = Column(Float, nullable=False)
    firsts = Column(Integer, nullable=False)
    failures = Column(Integer, nullable=False)
    scaling1 = Column(Integer, nullable=False)
    scaling2 = Column(Integer, nullable=False)
    scaling3 = Column(Integer, nullable=False)
    scaling4 = Column(Integer, nullable=False)
