from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox, QCheckBox, QLabel, QSpacerItem,
    QSizePolicy, QFileDialog, QListWidget, QCompleter
)
from PySide6.QtCore import Qt, QDate, QDateTime
import mysql.connector
from device_list import known_devices
from add_customer_form import AddCustomerForm
from user_context import current_user

class RepairIntakeForm(QDialog):
    def __init__(self, on_submit_callback=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Repair Intake Form")
        self.setFixedSize(460, 560)
        self.on_submit_callback = on_submit_callback
        self.customer_confirmed = False

        self.setModal(True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        # Input Fields
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Full Name (e.g. Jane Q. Doe)")

        self.customer_id_label = QLabel("")
        self.customer_id_label.setAlignment(Qt.AlignRight)
        self.customer_id_label.setStyleSheet("color: gray; font-size: 10pt;")
        self.customer_id_label.hide()

        self.device_type = QLineEdit()
        self.serial_number = QLineEdit()

        self.problem_description = QTextEdit()
        self.problem_description.setPlaceholderText("e.g. Describe customer's problem in detail")
        self.problem_description.setFixedHeight(50)

        self.condition_received = QTextEdit()
        self.condition_received.setPlaceholderText("e.g. Describe condition and visible damage")
        self.condition_received.setFixedHeight(40)

        self.internal_notes = QTextEdit()
        self.internal_notes.setFixedHeight(40)

        self.urgency_level = QComboBox()
        self.urgency_level.addItems(["Low", "Medium", "High"])

        self.priority_checkbox = QCheckBox("Mark as Priority")
        self.warranty_checkbox = QCheckBox("Under Warranty")

        self.intake_date = QDate.currentDate().toString("yyyy-MM-dd")
        self.intake_timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.date_label = QLabel(self.intake_date)
        self.timestamp_label = QLabel(self.intake_timestamp)
        self.intake_employee = QLabel(current_user.get("employee_id", "Unknown"))
        self.ticket_number = QLabel("TKT-" + QDate.currentDate().toString("yyyyMMdd"))

        self.image_list = QListWidget()
        self.upload_button = QPushButton("Upload Images")
        self.upload_button.clicked.connect(self.placeholder_upload_images)

        # Autocomplete setup
        device_completer = QCompleter(known_devices)
        device_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.device_type.setCompleter(device_completer)

        customer_names = self.get_customer_names()
        self.stored_customers = set(customer_names)
        customer_completer = QCompleter(customer_names)
        customer_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.customer_name.setCompleter(customer_completer)
        self.customer_name.textChanged.connect(self.update_customer_id_display)

        # Layout
        form_layout = QFormLayout()
        header_row = QHBoxLayout()
        header_row.addWidget(QLabel("Customer Name:"))
        header_row.addStretch()
        header_row.addWidget(self.customer_id_label)

        name_row = QHBoxLayout()
        name_row.addWidget(self.customer_name)

        form_layout.addRow(header_row)
        form_layout.addRow(name_row)
        form_layout.addItem(QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        form_layout.addRow("Device Type:", self.device_type)
        form_layout.addRow("Serial Number:", self.serial_number)
        form_layout.addRow("Problem:", self.problem_description)
        form_layout.addItem(QSpacerItem(10, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))
        form_layout.addRow("Condition Received:", self.condition_received)
        form_layout.addItem(QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        form_layout.addRow("Urgency:", self.urgency_level)
        form_layout.addRow(self.priority_checkbox)
        form_layout.addRow(self.warranty_checkbox)
        form_layout.addItem(QSpacerItem(10, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))
        form_layout.addRow("Internal Notes:", self.internal_notes)
        form_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        form_layout.addRow("Uploaded Images:", self.image_list)
        form_layout.addRow(self.upload_button)
        form_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        form_layout.addRow("Date of Intake:", self.date_label)
        form_layout.addRow("Timestamp:", self.timestamp_label)
        form_layout.addRow("Intake Employee:", self.intake_employee)
        form_layout.addRow("Ticket Number:", self.ticket_number)

        button_layout = QHBoxLayout()
        submit_btn = QPushButton("Submit")
        cancel_btn = QPushButton("Cancel")
        submit_btn.clicked.connect(self.submit)
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(cancel_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def get_customer_names(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="C0kec@ns",
                database="eisengut"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM customers")
            names = [row[0] for row in cursor.fetchall()]
            conn.close()
            return names
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            return []

    def update_customer_id_display(self):
        full_name = self.customer_name.text().strip()
        if not full_name:
            self.customer_id_label.hide()
            return
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="C0kec@ns",
                database="eisengut"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT customer_id FROM customers WHERE name = %s", (full_name,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self.customer_id_label.setText(f"Customer ID: {result[0]}")
                self.customer_id_label.show()
            else:
                self.customer_id_label.hide()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            self.customer_id_label.hide()

    def submit(self):
        full_name = self.customer_name.text().strip()
        device = self.device_type.text().strip()
        serial = self.serial_number.text().strip()
        problem = self.problem_description.toPlainText().strip()

        if not all([full_name, device, problem]):
            QMessageBox.warning(self, "Missing Info", "Please complete all required fields (Name, Device, Problem).")
            return

        if not self.customer_confirmed:
            if full_name not in self.stored_customers:
                choice = QMessageBox.question(
                    self,
                    "New Customer?",
                    "This customer is not in the system. Add new customer?",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )
                if choice == QMessageBox.Cancel:
                    return
                elif choice == QMessageBox.Yes:
                    form = AddCustomerForm(self)
                    form.name_input.setText(full_name)
                    if form.exec() == QDialog.Accepted:
                        self.stored_customers.add(full_name)
                        self.customer_name.setCompleter(QCompleter(list(self.stored_customers)))
                        self.customer_confirmed = True
                        self.update_customer_id_display()
                        QMessageBox.information(self, "Now Submit", "Customer added. Please press Submit again to complete the intake.")
                    return
                elif choice == QMessageBox.No:
                    confirm = QMessageBox.question(
                        self,
                        "Proceed Without Profile?",
                        "Would you like to save this intake without creating a customer profile?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if confirm == QMessageBox.No:
                        return
                    self.customer_confirmed = True
                    QMessageBox.information(self, "Now Submit", "Proceeding without customer profile. Please press Submit again to complete.")
                    return
            else:
                self.customer_confirmed = True

        data = {
            "customer_name": full_name,
            "device": device,
            "serial": serial,
            "problem": problem,
            "condition": self.condition_received.toPlainText().strip(),
            "urgency": self.urgency_level.currentText(),
            "priority": self.priority_checkbox.isChecked(),
            "warranty": self.warranty_checkbox.isChecked(),
            "internal_notes": self.internal_notes.toPlainText().strip(),
            "employee": current_user.get("employee_id", "Unknown"),
            "date": self.intake_date,
            "timestamp": self.intake_timestamp,
            "ticket": self.ticket_number.text()
        }

        if self.on_submit_callback:
            self.on_submit_callback(data)

        QMessageBox.information(self, "Saved", "Device intake has been saved.")
        self.accept()

    def placeholder_upload_images(self):
        QMessageBox.information(self, "Coming Soon", "Image uploads will be available in a future update.")

    def closeEvent(self, event):
        if any([
            self.customer_name.text().strip(),
            self.device_type.text().strip(),
            self.serial_number.text().strip(),
            self.problem_description.toPlainText().strip(),
            self.condition_received.toPlainText().strip(),
            self.internal_notes.toPlainText().strip()
        ]):
            confirm = QMessageBox.question(
                self,
                "Unsaved Work",
                "You have unsaved data. Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.No:
                event.ignore()
                return
        event.accept()

    def reject(self):
        self.close()
