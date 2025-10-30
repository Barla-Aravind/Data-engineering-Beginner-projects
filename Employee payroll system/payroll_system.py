import sqlite3

DB_NAME = 'employees.db'

# 2 : Create Tables

def create_tabels():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''
             CREATE TABLE IF NOT EXISTS Department (
                    dept_id INTEGER PRIMARY KEY,
                    dept_name TEXT NOT NULL
            )
        ''')
        cur.execute('''
                CREATE TABLE IF NOT EXISTS Employee (
                    emp_id INTEGER PRIMARY KEY,
                    name TEXT,
                    dept_id INTEGER,
                    basic_salary REAL,
                    bonus REAL,
                    tax REAl,
                    FOREIGN KEY(dept_id) REFERENCES Department(dept_id)
                )
        ''')
    print("Tables Created Successfully")

# 3 : Insert Data into tables

def insert_data():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()

        departments = [
            (1, 'HR'),
            (2, 'IT'),
            (3, 'Finance')
        ]
        cur.executemany("INSERT OR IGNORE INTO Department VALUES(?, ?)", departments)
                        
        employees = [
            (1, 'Aravind', 2, 50000, 5000, 2000),
            (2, 'Siri',3, 60000, 6000, 2500),
            (3, 'Rahul',1, 40000, 3000, 1500)
        ]
        cur.executemany("INSERT OR REPLACE INTO Employee VALUES (?, ?, ?, ?, ?, ?)", employees)

    print("Sample Data Inserted")

# step 4 : View all employees with their department

def view_employees():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT  e.emp_id, e.name, d.dept_name, e.basic_salary, e.bonus, e.tax 
        FROM Employee e 
        JOIN Department d ON e.dept_id = d.dept_id''')

        rows = cur.fetchall()
    print("\n Employee Details:")
    print("ID | Name | Department | Salary | Bonus | Tax")
    for row in rows:
        print(row)

# step 5 : Calculate Total Salary (basic + bonus - tax)

def calculate_total_salary():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''
        SELECT name, (basic_salary + bonus - tax) AS total_salary FROM Employee''')
        rows = cur.fetchall()

    print("\n Total salary after bonus and tax:")
    for name, total in rows:
        print(f"{name}: ₹{total}")

# Step 6: Update or Delete Employee

def update_salary(emp_id, new_salary):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE Employee SET basic_salary = ? WHERE emp_id = ?", (new_salary, emp_id))
    print(" Salary Updated")

def delete_employee(emp_id):
    with sqlite3.conect(DB_NAME) as conn :
        cur = conn.cursor()
        cur.execute("DELETE FROM Employee WHERE emp_id n= ?", (emp_id))
    print(" Employee Deleted")

# Step 7 : Run $ Test all 
if __name__ == '__main__':
    create_tabels()
    insert_data()
    view_employees()
    calculate_total_salary()

#Example  update usage
    update_salary(1, 55000)
    view_employees( )

#Example delete usage
    delete_employee(1)
    view_employees()