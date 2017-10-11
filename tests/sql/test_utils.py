"""Tests for sql.utils module."""
import pytest
from mock import patch
from sql.utils import session_scope


@patch('sql.utils.SESSION')
def test_session_scope(mock_session_factory):
    """Test the session_scope."""
    # Try normal (non exception raising) operation
    with session_scope('engine') as session:
        mock_session_factory.assert_called_with(bind='engine')
    session.commit.assert_called()
    session.rollback.assert_not_called()
    session.close.assert_called()

    # Try exception raising incident
    mock_session_factory.reset_mock()
    with pytest.raises(RuntimeError), session_scope('engine') as session:
        mock_session_factory.assert_called_with(bind='engine')
        raise RuntimeError
    session.commit.assert_not_called()
    session.rollback.assert_called()
    session.close.assert_called()
