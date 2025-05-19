import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="C0kec@ns",
    database="eisengut"
)

cursor = conn.cursor()

# Add employee 9101
cursor.execute("""
INSERT INTO employees (name, employee_number, role)
VALUES (%s, %s, %s)
""", ("Test User", "9101", "Dispatcher"))

conn.commit()
cursor.close()
conn.close()

print("Employee 9101 added.")
