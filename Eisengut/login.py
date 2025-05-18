from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from user_context import current_user

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

        # Pressing Enter triggers login
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

        current_user["employee_id"] = employee_id
        self.on_login_success()
        self.close()
