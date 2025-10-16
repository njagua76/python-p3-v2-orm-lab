from lib import CONN, CURSOR
from lib.employee import Employee
from lib.review import Review

# Reset tables
Employee.drop_table()
Review.drop_table()
Employee.create_table()
Review.create_table()

# Create sample data
emp1 = Employee.create("Ann Gathoni", "Data Analyst")
emp2 = Employee.create("Joseph Ndiritu", "Backend Engineer")

rev1 = Review.create(2023, "Excellent performance and team contribution.", emp1.id)
rev2 = Review.create(2024, "Strong technical growth and leadership.", emp1.id)
rev3 = Review.create(2023, "Needs improvement in time management.", emp2.id)

print("All Reviews:", Review.get_all())
print("Ann's Reviews:", emp1.reviews())
