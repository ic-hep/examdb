"""SQLAlchemy Users Module."""
from sqlalchemy import Column, Integer, String, Boolean
from .Base import Base


class Users(Base):
    """Users table."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    cid = Column(String(8), nullable=False)
    username = Column(String(20), nullable=False)
    email = Column(String(40), nullable=False)
    admin = Column(Boolean, nullable=False)
