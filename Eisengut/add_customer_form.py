from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox
)
import mysql.connector
import random
import re

class AddCustomerForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Customer")
        self.setFixedSize(400, 180)

        # Input fields
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        # Layouts
        form_layout = QFormLayout()
        form_layout.addRow("Full Name:", self.name_input)
        form_layout.addRow("Phone Number:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Address:", self.address_input)

        # Buttons
        button_layout = QHBoxLayout()
        submit_btn = QPushButton("Add Customer")
        cancel_btn = QPushButton("Cancel")
        submit_btn.clicked.connect(self.submit)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(cancel_btn)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def submit(self):
        full_name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not full_name:
            QMessageBox.warning(self, "Missing Name", "Customer name is required.")
            return

        base_id = re.sub(r'[^A-Za-z]', '', full_name.split()[-1].upper()[:3])
        base_id = base_id.ljust(3, 'X')
        customer_id = None

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="C0kec@ns",
                database="eisengut"
            )
            cursor = conn.cursor()

            for _ in range(10):
                num = random.randint(100, 999)
                temp_id = f"{base_id}{num}"
                cursor.execute("SELECT COUNT(*) FROM customers WHERE customer_id = %s", (temp_id,))
                if cursor.fetchone()[0] == 0:
                    customer_id = temp_id
                    break

            if not customer_id:
                raise Exception("Unable to generate unique customer ID after 10 tries.")

            cursor.execute("""
                INSERT INTO customers (
                    customer_id, name, phone, email, address
                ) VALUES (%s, %s, %s, %s, %s)
            """, (customer_id, full_name, phone, email, address))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", f"Customer '{full_name}' added with ID {customer_id}.")
            self.accept()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", str(err))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
