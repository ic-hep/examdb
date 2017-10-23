"""Tests for sql.tables.__init__ module."""
from mock import patch
import examlib.sql.tables as tables


def test_table_imports():
    """Test table imports."""
    namespace = vars(tables)
    for i in ('Base',
              'Students',
              'Users',
              'Courses',
              'CourseAliases',
              'CourseHistory',
              'Marks',
              'Options'):
        assert i in namespace


@patch('examlib.sql.tables.rebind_session')
@patch('examlib.sql.tables.Base')
@patch('examlib.sql.tables.create_engine')
def test_create_all_tables(create_engine, Base, rebind_session):
    """Test create_all_tables."""
    url = 'sqlite://'
    tables.create_all_tables(url)
    create_engine.assert_called_with(url)
    Base.metadata.create_all.assert_called_with(bind=create_engine())
    rebind_session.assert_called_with(create_engine())
