from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from login import LoginWindow
from user_context import current_user
from home_screen import HomeScreenWidget
from repair_intake_form import RepairIntakeForm
from add_customer_form import AddCustomerForm
from customer_list import CustomerListWindow  # NEW IMPORT

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
                padding: 1px 1px;
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
            a.triggered.connect(handler)
            return a

        dashboard = menu_bar.addMenu("Dashboard")
        dashboard.addAction(action("Overview", lambda: self.show_message("Overview")))
        dashboard.addAction(action("Daily Job Summary", lambda: self.show_message("Daily Job Summary")))
        dashboard.addAction(action("System Status", lambda: self.show_message("System Status")))

        customers = menu_bar.addMenu("Customers")
        customers.addAction(action("Customer List", self.open_customer_list_window))  # UPDATED
        customers.addAction(action("Add New Customer", self.open_add_customer_form))
        customers.addAction(action("Contact History / Notes", lambda: self.show_message("Contact History / Notes")))

        repairs = menu_bar.addMenu("Repairs")
        repairs.addAction(action("Open Repair Tickets", lambda: self.show_message("Open Repair Tickets")))
        repairs.addAction(action("Create New Ticket", lambda: self.show_message("Create New Ticket")))
        repairs.addAction(action("Completed Repairs", lambda: self.show_message("Completed Repairs")))
        repairs.addAction(action("Warranty Tracker", lambda: self.show_message("Warranty Tracker")))

        billing = menu_bar.addMenu("Billing")
        billing.addAction(action("Add/Remove Quotes", lambda: self.show_message("Add/Remove Quotes")))
        billing.addAction(action("Invoices", lambda: self.show_message("Invoices")))
        billing.addAction(action("Payments Received", lambda: self.show_message("Payments Received")))
        billing.addAction(action("Unpaid/Overdue Accounts", lambda: self.show_message("Unpaid/Overdue Accounts")))

        inventory = menu_bar.addMenu("Inventory")
        inventory.addAction(action("Parts List", lambda: self.show_message("Parts List")))
        inventory.addAction(action("Stock Levels", lambda: self.show_message("Stock Levels")))
        inventory.addAction(action("Add/Remove Part", lambda: self.show_message("Add/Remove Part")))
        inventory.addAction(action("Order History", lambda: self.show_message("Order History")))

        staff = menu_bar.addMenu("Staff")
        staff.addAction(action("Staff Directory", lambda: self.show_message("Staff Directory")))
        staff.addAction(action("Assign Jobs", lambda: self.show_message("Assign Jobs")))
        staff.addAction(action("Hours Worked", lambda: self.show_message("Hours Worked")))
        staff.addAction(action("Add New Technician", lambda: self.show_message("Add New Technician")))

        devices = menu_bar.addMenu("Devices")
        devices.addAction(action("Device Intake Form", self.open_device_intake_form))
        devices.addAction(action("Manufacturer Info", lambda: self.show_message("Manufacturer Info")))
        devices.addAction(action("Repair Guides", lambda: self.show_message("Repair Guides")))
        devices.addAction(action("Return Status", lambda: self.show_message("Return Status")))

        reports = menu_bar.addMenu("Reports")
        reports.addAction(action("Daily / Weekly / Monthly Summary", lambda: self.show_message("Summary Report")))
        reports.addAction(action("Revenue Breakdown", lambda: self.show_message("Revenue Breakdown")))
        reports.addAction(action("Most Common Repairs", lambda: self.show_message("Most Common Repairs")))
        reports.addAction(action("Technician Performance", lambda: self.show_message("Technician Performance")))

        tools = menu_bar.addMenu("Tools")
        tools.addAction(action("Label Generator", lambda: self.show_message("Label Generator")))
        tools.addAction(action("Backup/Export Database", lambda: self.show_message("Backup/Export Database")))
        tools.addAction(action("Settings / Preferences", lambda: self.show_message("Settings / Preferences")))

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction(action("User Manual", lambda: self.show_message("User Manual")))
        help_menu.addAction(action("Contact Admin", lambda: self.show_message("Contact Admin")))
        help_menu.addAction(action("About", lambda: self.show_message("About")))

    def show_message(self, title):
        QMessageBox.information(self, title, f"{title} clicked.")

    def open_device_intake_form(self):
        form = RepairIntakeForm()
        form.exec()

    def open_add_customer_form(self):
        form = AddCustomerForm(self)
        form.exec()

    def open_customer_list_window(self):  # NEW METHOD
        form = CustomerListWindow(self)
        form.exec()

def launch_main():
    global main_window
    main_window = MainWindow()
    main_window.show()

if __name__ == "__main__":
    app = QApplication([])

    login_window = LoginWindow(on_login_success=launch_main)
    login_window.show()

    app.exec()
