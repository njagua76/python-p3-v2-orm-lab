from lib import CURSOR, CONN

class Employee:
    all = {}

    def __init__(self, name, job_title, id=None):
        self.id = id
        self.name = name
        self.job_title = job_title

    def __repr__(self):
        return f"<Employee {self.id}: {self.name}, {self.job_title}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                job_title TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS employees;")
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO employees (name, job_title) VALUES (?, ?);",
                (self.name, self.job_title)
            )
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        else:
            self.update()

    def update(self):
        CURSOR.execute(
            "UPDATE employees SET name = ?, job_title = ? WHERE id = ?;",
            (self.name, self.job_title, self.id)
        )
        CONN.commit()

    @classmethod
    def create(cls, name, job_title):
        emp = cls(name, job_title)
        emp.save()
        return emp

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM employees WHERE id = ?;"
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            emp = cls.all.get(row[0])
            if not emp:
                emp = cls(row[1], row[2], row[0])
                cls.all[emp.id] = emp
            return emp
        return None

    #  Relationship to Reviews
    def reviews(self):
        from lib.review import Review  # avoid circular import
        sql = "SELECT * FROM reviews WHERE employee_id = ?;"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Review.instance_from_db(row) for row in rows]

