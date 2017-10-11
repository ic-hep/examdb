"""SQLAlchemy Courses Module."""
from sqlalchemy import Column, Integer, String, ForeignKey
from .Base import Base


class Courses(Base):
    """Courses table."""

    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(String(30), nullable=False)
    year = Column(Integer, nullable=False)
    primary_contact = Column(Integer, ForeignKey("users.id"))
    scaling1 = Column(Integer)
    scaling2 = Column(Integer)
    scaling3 = Column(Integer)
    scaling4 = Column(Integer)
