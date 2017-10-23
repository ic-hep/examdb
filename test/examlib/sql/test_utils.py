"""Tests for sql.utils module."""
import pytest
from mock import Mock, patch
from examlib.sql.utils import rebind_session, db_session


@patch('examlib.sql.utils.SESSION')
def test_rebind_session(SESSION):
    """Test the session rebinding."""
    engine = Mock()
    rebind_session(engine)
    SESSION.remove.assert_called()
    SESSION.configure.assert_called_with(bind=engine)


@patch('examlib.sql.utils.create_engine')
@patch('examlib.sql.utils.SESSION')
@patch('examlib.sql.utils.rebind_session')
def test_db_session(rebind_session, SESSION, create_engine):
    """Test the DB session context."""
    # Try normal (non exception raising) operation
    with db_session() as _:
        rebind_session.assert_not_called()
    SESSION.commit.assert_called()
    SESSION.rollback.assert_not_called()
    SESSION.remove.assert_called()

    # Try exception raising incident
    rebind_session.reset_mock()
    SESSION.reset_mock()
    with pytest.raises(RuntimeError), db_session() as _:
        rebind_session.assert_not_called()
        raise RuntimeError
    SESSION.commit.assert_not_called()
    SESSION.rollback.assert_called()
    SESSION.remove.assert_called()

    # Try exception swallowing incident
    rebind_session.reset_mock()
    SESSION.reset_mock()
    with db_session(reraise=False) as _:
        rebind_session.assert_not_called()
        raise RuntimeError
    SESSION.commit.assert_not_called()
    SESSION.rollback.assert_called()
    SESSION.remove.assert_called()

    # Try rebinding of session
    rebind_session.reset_mock()
    SESSION.reset_mock()
    url = 'sqlite://'
    with db_session(url=url) as _:
        create_engine.assert_called_with(url)
        rebind_session.assert_called_with(create_engine())
    SESSION.commit.assert_called()
    SESSION.rollback.assert_not_called()
    SESSION.remove.assert_called()
