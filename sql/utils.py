"""SQLAlchemy Helpers."""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .tables import Base


SESSION = sessionmaker()


def create_all_tables(url):
    """Create all tables of type Base."""
    Base.metadata.create_all(bind=create_engine(url))


@contextmanager
def session_scope(url):
    """Provide a transactional scope around a series of operations."""
    session = SESSION(bind=create_engine(url))
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
