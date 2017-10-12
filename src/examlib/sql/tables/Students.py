"""SQLAlchemy Students Module."""
from sqlalchemy import Column, Integer, String, Float
from .Base import Base


class Students(Base):
    """Students table."""

    __tablename__ = "students"
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    cid = Column(String(8), nullable=False)
    firstname = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    current_year = Column(Integer)
    year1_average = Column(Float)
    year12_average = Column(Float)
