from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QAbstractItemView, QLineEdit, QComboBox,
    QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
import mysql.connector

from add_customer_form import AddCustomerForm


class CustomerListWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Customer List")
        self.setFixedHeight(540)

        self.layout = QVBoxLayout(self)

        # Search bar and dropdown
        search_bar_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.returnPressed.connect(self.apply_filter)
        search_bar_layout.addWidget(self.search_input)

        self.search_dropdown = QComboBox()
        self.search_dropdown.addItem("Search All")
        self.search_dropdown.addItem("Name")
        self.search_dropdown.addItem("Phone")
        self.search_dropdown.addItem("Email")
        self.search_dropdown.addItem("Address")
        self.search_dropdown.addItem("Customer ID")
        search_bar_layout.addWidget(self.search_dropdown)

        self.layout.addLayout(search_bar_layout)

        # Table
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table.verticalHeader().setDefaultSectionSize(16)
        self.layout.addWidget(self.table)

        # Internal state
        self.original_value = None
        self.columns = []
        self.all_rows = []
        self.selected_row = None
        self._resized_once = False

        # Table events
        self.table.cellDoubleClicked.connect(self.store_original_value)
        self.table.cellChanged.connect(self.confirm_cell_change)
        self.table.cellClicked.connect(self.track_selection)

        # Bottom: Add + Delete buttons (centered)
        button_bar = QHBoxLayout()
        button_bar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.add_btn = QPushButton("Add Customer")
        self.add_btn.clicked.connect(self.open_add_customer_form)
        button_bar.addWidget(self.add_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_customer)
        self.delete_btn.setAutoDefault(False)
        self.delete_btn.setDefault(False)
        button_bar.addWidget(self.delete_btn)

        button_bar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(button_bar)

        self.load_customers()

    def track_selection(self, row, column):
        self.selected_row = row

    def store_original_value(self, row, column):
        col_name = self.columns[column]
        if col_name != "id":
            self.original_value = self.table.item(row, column).text()
        else:
            self.original_value = None

    def confirm_cell_change(self, row, column):
        col_name = self.columns[column]
        if col_name == "id" or self.original_value is None:
            return

        new_value = self.table.item(row, column).text()
        if new_value != self.original_value:
            customer_id = self.table.item(row, self.columns.index("id")).text()

            confirm = QMessageBox.question(
                self, "Confirm Update",
                f"Update '{col_name}' for customer #{customer_id} to:\n\n{new_value}?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                try:
                    conn = mysql.connector.connect(
                        host="localhost", user="root", password="C0kec@ns", database="eisengut"
                    )
                    cursor = conn.cursor()
                    query = f"UPDATE customers SET {col_name}=%s WHERE id=%s"
                    cursor.execute(query, (new_value, customer_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    QMessageBox.information(self, "Updated", f"{col_name} updated.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Update failed:\n{e}")
            else:
                self.table.blockSignals(True)
                self.table.item(row, column).setText(self.original_value)
                self.table.blockSignals(False)

        self.original_value = None

    def load_customers(self):
        self.table.setRowCount(0)
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="C0kec@ns", database="eisengut"
            )
            cursor = conn.cursor()

            cursor.execute("DESCRIBE customers")
            self.columns = [row[0] for row in cursor.fetchall()]
            self.table.setColumnCount(len(self.columns))
            self.table.setHorizontalHeaderLabels(self.columns)

            cursor.execute("SELECT * FROM customers")
            self.all_rows = cursor.fetchall()

            cursor.close()
            conn.close()

            self.refresh_table(self.all_rows)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load customers:\n{e}")

    def refresh_table(self, data_rows):
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data_rows):
            self.table.insertRow(row_idx)
            self.table.setRowHeight(row_idx, 16)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if self.columns[col_idx] == "id":
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)

        self.table.resizeColumnsToContents()

        if not self._resized_once:
            total_width = sum([self.table.columnWidth(i) for i in range(self.table.columnCount())])
            self.resize(total_width + 40, self.height())
            self._resized_once = True

    def apply_filter(self):
        term = self.search_input.text().lower().strip()
        mode = self.search_dropdown.currentText()
        filtered = []

        for row in self.all_rows:
            row_dict = dict(zip(self.columns, [str(cell).lower() for cell in row]))
            if mode == "Search All":
                if any(term in value for value in row_dict.values()):
                    filtered.append(row)
            else:
                column_map = {
                    "Name": "name",
                    "Phone": "phone",
                    "Email": "email",
                    "Address": "address",
                    "Customer ID": "customer_id"
                }
                col_key = column_map.get(mode)
                if col_key and term in row_dict.get(col_key, ""):
                    filtered.append(row)

        self.refresh_table(filtered)

    def delete_customer(self):
        if self.selected_row is None:
            QMessageBox.warning(self, "No Selection", "Select a customer to delete.")
            return

        cust_id = self.table.item(self.selected_row, self.columns.index("id")).text()
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete customer #{cust_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="C0kec@ns", database="eisengut"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM customers WHERE id=%s", (cust_id,))
                conn.commit()
                cursor.close()
                conn.close()
                self.load_customers()
                self.selected_row = None
                QMessageBox.information(self, "Deleted", "Customer deleted.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Delete failed:\n{e}")

    def open_add_customer_form(self):
        form = AddCustomerForm(self)
        if form.exec() == QDialog.Accepted:
            self.load_customers()
