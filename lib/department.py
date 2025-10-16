from lib import CONN, CURSOR
from lib.employee import Employee


class Department:
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Department {self.id}: {self.name}>"

    # -----------------------------------------------------
    # 🗂 Table Management
    # -----------------------------------------------------

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments;"
        CURSOR.execute(sql)
        CONN.commit()

    # -----------------------------------------------------
    # 🧩 ORM Methods
    # -----------------------------------------------------

    def save(self):
        """Insert new or update existing department"""
        if self.id is None:
            CURSOR.execute("INSERT INTO departments (name) VALUES (?);", (self.name,))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        else:
            self.update()

    @classmethod
    def create(cls, name):
        dept = cls(name)
        dept.save()
        return dept

    @classmethod
    def instance_from_db(cls, row):
        """Return a Department instance from a database row."""
        dept = cls.all.get(row[0])
        if dept:
            dept.name = row[1]
        else:
            dept = cls(row[1], row[0])
            cls.all[dept.id] = dept
        return dept

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?;"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM departments;"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def update(self):
        sql = "UPDATE departments SET name = ? WHERE id = ?;"
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM departments WHERE id = ?;"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    # -----------------------------------------------------
    # Relationship: Employees in this Department
    # -----------------------------------------------------

    def employees(self):
        """Return list of Employee instances belonging to this department."""
        sql = "SELECT * FROM employees WHERE department_id = ?;"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()

        employees = []
        for row in rows:
            emp = Employee.all.get(row[0])
            if not emp:
                emp = Employee(row[1], row[2], row[0])
                Employee.all[emp.id] = emp
            employees.append(emp)
        return employees
