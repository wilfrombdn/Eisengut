from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from user_context import current_user
import mysql.connector
from mysql.connector import Error

class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.setWindowTitle("Eisengut")
        self.setFixedSize(225, 100)
        self.on_login_success = on_login_success

        layout = QVBoxLayout()

        self.label = QLabel("Enter Employee Number:")
        self.input = QLineEdit()
        self.input.setPlaceholderText("e.g. 1051")
        self.input.returnPressed.connect(self.submit_login)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.submit_login)

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def submit_login(self):
        employee_id = self.input.text().strip()
        if not employee_id.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Employee number must be digits only.")
            return

        if self.verify_employee_in_database(employee_id):
            current_user["employee_id"] = employee_id
            self.on_login_success()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", f"Employee #{employee_id} not found in system.")

    def verify_employee_in_database(self, emp_number):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="C0kec@ns",
                database="eisengut"
            )
            cursor = conn.cursor()
            query = "SELECT id FROM employees WHERE employee_number = %s"
            cursor.execute(query, (emp_number,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result is not None
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to connect to database.\n\n{e}")
            return False
