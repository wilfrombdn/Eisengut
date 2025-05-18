# home_screen.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from user_context import current_user

# Temporary assignment data
def get_user_assignments(emp_id):
    dummy_data = {
        "9101": [
            "Q12589 - QUOTE ACCEPTED TRANSITION TO WORK ORDER",
            "WO#6181 - OPEN",
            "WO#2185 - OPEN",
            "WO#0571 - OVERDUE"
        ],
        "0001": ["WO#9999 - OPEN"]
    }
    return dummy_data.get(emp_id, ["No assignments found."])

class HomeScreenWidget(QWidget):
    def __init__(self):
        super().__init__()

        emp_id = current_user.get("employee_id", "Unknown")
        assignments = get_user_assignments(emp_id)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Assignments for Employee #{emp_id}:"))

        assignment_list = QListWidget()
        assignment_list.setFixedWidth(320)  # 1/4 of 1280px window width

        for task in assignments:
            item = QListWidgetItem(task)
            assignment_list.addItem(item)

        layout.addWidget(assignment_list)
        self.setLayout(layout)
