from lib.department import Department
from lib.employee import Employee

class TestDepartment:
    def test_create_and_find(self):
        d = Department.create("IT", "Nairobi")
        assert d.id is not None
        found = Department.find_by_name("IT")
        assert found.name == "IT"

    def test_update_department(self):
        d = Department.create("Finance", "Mombasa")
        d.location = "Nakuru"
        d.update()
        found = Department.find_by_id(d.id)
        assert found.location == "Nakuru"

    def test_employees_relationship(self):
        d = Department.create("HR", "Kisumu")
        e1 = Employee.create("Ann", "Manager", d.id)
        e2 = Employee.create("John", "Assistant", d.id)
        employees = d.employees()
        assert len(employees) == 2
        assert employees[0].department_id == d.id
