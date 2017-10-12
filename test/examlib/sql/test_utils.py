"""Tests for sql.utils module."""
import pytest
from mock import Mock
from examlib.sql.utils import scoped_session


def test_scoped_session():
    """Test the session_scope."""
    # Try normal (non exception raising) operation
    mock_session_factory = Mock()
    with scoped_session(mock_session_factory) as session:
        mock_session_factory.assert_called()
    session.commit.assert_called()
    session.rollback.assert_not_called()
    session.close.assert_called()

    # Try exception raising incident
    mock_session_factory.reset_mock()
    with pytest.raises(RuntimeError),\
         scoped_session(mock_session_factory) as session:
        mock_session_factory.assert_called()
        raise RuntimeError
    session.commit.assert_not_called()
    session.rollback.assert_called()
    session.close.assert_called()

    # Try exception swallowing incident
    mock_session_factory.reset_mock()
    with scoped_session(mock_session_factory, reraise=False) as session:
        mock_session_factory.assert_called()
        raise RuntimeError
    session.commit.assert_not_called()
    session.rollback.assert_called()
    session.close.assert_called()
