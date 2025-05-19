# home_screen.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QSize, QTimer
import mysql.connector
from mysql.connector import Error
from user_context import current_user


# Small colored circle widget (green/red)
class ConnectionIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.connected = False
        self.setFixedSize(QSize(12, 12))

    def set_connected(self, status):
        self.connected = status
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        color = QColor(0, 200, 0) if self.connected else QColor(200, 0, 0)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawEllipse(0, 0, 12, 12)


def is_mysql_connected():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="C0kec@ns"
        )
        if conn.is_connected():
            conn.close()
            return True
    except Error:
        return False
    return False


# Dummy assignment data
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
        assignment_list.setFixedWidth(320)
        for task in assignments:
            item = QListWidgetItem(task)
            assignment_list.addItem(item)
        layout.addWidget(assignment_list)

        # Connection status bar (bottom right)
        self.status_layout = QHBoxLayout()
        self.status_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.status_label = QLabel("Connected to data server")
        self.indicator = ConnectionIndicator()
        self.status_layout.addWidget(self.status_label)
        self.status_layout.addWidget(self.indicator)
        layout.addLayout(self.status_layout)

        # Timer for periodic connection check
        self.connection_timer = QTimer(self)
        self.connection_timer.timeout.connect(self.check_connection)
        self.connection_timer.start(5000)  # every 5 seconds

        # First check
        self.check_connection()

        self.setLayout(layout)

    def check_connection(self):
        status = is_mysql_connected()
        self.indicator.set_connected(status)
