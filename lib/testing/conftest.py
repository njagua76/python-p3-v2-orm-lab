import pytest
from lib import CONN, CURSOR
from lib.department import Department
from lib.employee import Employee

@pytest.fixture(autouse=True)
def reset_db():
    """Drop and recreate tables before every test"""
    Employee.drop_table()
    Department.drop_table()
    Department.create_table()
    Employee.create_table()
    yield
    CONN.commit()
