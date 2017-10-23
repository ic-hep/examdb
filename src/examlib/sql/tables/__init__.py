"""SQLAlchemy Tables Package."""
from sqlalchemy import create_engine
from .Base import Base
from .Students import Students
from .Users import Users
from .Courses import Courses
from .CourseAliases import CourseAliases
from .CourseHistory import CourseHistory
from .Marks import Marks
from .Options import Options

from ..utils import rebind_session


def create_all_tables(url):
    """Create all SQLAlchemy tables."""
    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)
    rebind_session(engine)
