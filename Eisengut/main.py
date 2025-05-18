from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from login import LoginWindow
from user_context import current_user
from home_screen import HomeScreenWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        emp_id = current_user.get("employee_id", "Unknown")

        self.setWindowTitle(f"Eisengut - Logged in as #{emp_id}")
        self.setFixedSize(1280, 720)
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowTitleHint |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint
        )

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QMenuBar {
                background-color: #dcdcdc;
                border: 1px solid #a0a0a0;
            }
            QMenuBar::item {
                background: transparent;
                padding: 4px 10px;
                margin: 1px;
            }
            QMenuBar::item:selected {
                background: #c0c0c0;
            }
            QMenu {
                background-color: #f0f0f0;
                border: 1px solid #a0a0a0;
            }
            QMenu::item {
                padding: 4px 20px;
                margin: 1px;
            }
            QMenu::item:selected {
                background-color: #a0a0a0;
                color: black;
            }
        """)

        self.setup_menu_bar()
        self.setCentralWidget(HomeScreenWidget())

    def setup_menu_bar(self):
        menu_bar = self.menuBar()

        def action(label, handler):
            a = QAction(label, self)
            a.triggered.connect(lambda: QMessageBox.information(self, label, f"{label} clicked."))
            return a

        dashboard = menu_bar.addMenu("Dashboard")
        dashboard.addAction(action("Overview", self))
        dashboard.addAction(action("Daily Job Summary", self))
        dashboard.addAction(action("System Status", self))

        customers = menu_bar.addMenu("Customers")
        customers.addAction(action("Customer List", self))
        customers.addAction(action("Add New Customer", self))
        customers.addAction(action("Contact History / Notes", self))

        repairs = menu_bar.addMenu("Repairs")
        repairs.addAction(action("Open Repair Tickets", self))
        repairs.addAction(action("Create New Ticket", self))
        repairs.addAction(action("Completed Repairs", self))
        repairs.addAction(action("Warranty Tracker", self))

        billing = menu_bar.addMenu("Billing")
        billing.addAction(action("Add/Remove Quotes", self))
        billing.addAction(action("Invoices", self))
        billing.addAction(action("Payments Received", self))
        billing.addAction(action("Unpaid/Overdue Accounts", self))

        inventory = menu_bar.addMenu("Inventory")
        inventory.addAction(action("Parts List", self))
        inventory.addAction(action("Stock Levels", self))
        inventory.addAction(action("Add/Remove Part", self))
        inventory.addAction(action("Order History", self))

        staff = menu_bar.addMenu("Staff")
        staff.addAction(action("Staff Directory", self))
        staff.addAction(action("Assign Jobs", self))
        staff.addAction(action("Hours Worked", self))
        staff.addAction(action("Add New Technician", self))

        devices = menu_bar.addMenu("Devices")
        devices.addAction(action("Device Intake Form", self))
        devices.addAction(action("Manufacturer Info", self))
        devices.addAction(action("Repair Guides", self))
        devices.addAction(action("Return Status", self))

        reports = menu_bar.addMenu("Reports")
        reports.addAction(action("Daily / Weekly / Monthly Summary", self))
        reports.addAction(action("Revenue Breakdown", self))
        reports.addAction(action("Most Common Repairs", self))
        reports.addAction(action("Technician Performance", self))

        tools = menu_bar.addMenu("Tools")
        tools.addAction(action("Label Generator", self))
        tools.addAction(action("Backup/Export Database", self))
        tools.addAction(action("Settings / Preferences", self))

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction(action("User Manual", self))
        help_menu.addAction(action("Contact Admin", self))
        help_menu.addAction(action("About", self))

def launch_main():
    global main_window
    main_window = MainWindow()
    main_window.show()

if __name__ == "__main__":
    app = QApplication([])

    login_window = LoginWindow(on_login_success=launch_main)
    login_window.show()

    app.exec()
