"""SQLAlchemy Helpers."""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .tables import Base


SESSION = sessionmaker()


def create_all_tables(url):
    """Create all tables of type Base."""
    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)
    return engine


@contextmanager
def session_scope(engine):
    """Provide a transactional scope around a series of operations."""
    session = SESSION(bind=engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
