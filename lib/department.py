from __init__ import CONN, CURSOR

class Department:
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    # ---------------- PROPERTY VALIDATIONS ----------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not isinstance(value, str):
            raise ValueError("Location must be a string")
        if len(value.strip()) == 0:
            raise ValueError("Location cannot be empty")
        self._location = value

    # ---------------- DATABASE METHODS ----------------
    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        CONN.commit()

    def save(self):
        if self.id:
            self.update()
        else:
            sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.location))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self

    @classmethod
    def create(cls, name, location):
        dept = cls(name, location)
        dept.save()
        return dept

    def update(self):
        sql = "UPDATE departments SET name = ?, location = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    # ---------------- CLASSMETHODS FOR FINDING ----------------
    @classmethod
    def instance_from_db(cls, row):
        dept = cls.all.get(row[0])
        if dept:
            dept.name = row[1]
            dept.location = row[2]
        else:
            dept = cls(row[1], row[2], row[0])
            cls.all[row[0]] = dept
        return dept

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM departments").fetchall()
        return [cls.instance_from_db(row) for row in rows]

    # ---------------- RELATIONSHIP ----------------
    def employees(self):
        from employee import Employee
        sql = "SELECT * FROM employees WHERE department_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Employee.instance_from_db(row) for row in rows]
