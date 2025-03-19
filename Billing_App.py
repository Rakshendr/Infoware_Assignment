import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, QComboBox)
import mysql.connector
from datetime import datetime

class BillingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.init_db()
        self.load_customers()

    def init_ui(self):
        # Customer Input
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        self.save_customer_button = QPushButton("Save Customer")

        # Bill Input
        self.customer_combo = QComboBox()
        self.bill_date_label = QLabel("Bill Date:")
        self.bill_date_input = QDateEdit()
        self.bill_date_input.setDate(datetime.now().date())
        self.product_label = QLabel("Product:")
        self.product_input = QLineEdit()
        self.total_amount_label = QLabel("Total Amount:")
        self.total_amount_input = QLineEdit()
        self.save_bill_button = QPushButton("Save Bill")

        # View Buttons
        self.view_customers_button = QPushButton("View Customers")
        self.view_bills_button = QPushButton("View Bills")

        # Tables
        self.customers_table = QTableWidget()
        self.bills_table = QTableWidget()

        # Layouts
        customer_layout = QVBoxLayout()
        customer_layout.addWidget(self.name_label)
        customer_layout.addWidget(self.name_input)
        customer_layout.addWidget(self.address_label)
        customer_layout.addWidget(self.address_input)
        customer_layout.addWidget(self.phone_label)
        customer_layout.addWidget(self.phone_input)
        customer_layout.addWidget(self.save_customer_button)

        bill_layout = QVBoxLayout()
        bill_layout.addWidget(QLabel("Customer:"))
        bill_layout.addWidget(self.customer_combo)
        bill_layout.addWidget(self.bill_date_label)
        bill_layout.addWidget(self.bill_date_input)
        bill_layout.addWidget(self.product_label)
        bill_layout.addWidget(self.product_input)
        bill_layout.addWidget(self.total_amount_label)
        bill_layout.addWidget(self.total_amount_input)
        bill_layout.addWidget(self.save_bill_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.view_customers_button)
        button_layout.addWidget(self.view_bills_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(customer_layout)
        main_layout.addLayout(bill_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.customers_table)
        main_layout.addWidget(self.bills_table)

        self.setLayout(main_layout)
        self.setWindowTitle("Billing System")

        # Connect Buttons
        self.save_customer_button.clicked.connect(self.save_customer)
        self.save_bill_button.clicked.connect(self.save_bill)
        self.view_customers_button.clicked.connect(self.view_customers)
        self.view_bills_button.clicked.connect(self.view_bills)

    def init_db(self):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Rkc@1249",
                database="billing_system"
            )
            self.mycursor = self.mydb.cursor()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error connecting to database: {err}")
            sys.exit()

    def load_customers(self):
        self.mycursor.execute("SELECT customer_id, name FROM customers")
        results = self.mycursor.fetchall()
        self.customer_combo.clear()
        for customer_id, name in results:
            self.customer_combo.addItem(name, customer_id)

    def save_customer(self):
        name = self.name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()

        sql = "INSERT INTO customers (name, address, phone) VALUES (%s, %s, %s)"
        val = (name, address, phone)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        QMessageBox.information(self, "Success", "Customer saved successfully.")
        self.clear_inputs()
        self.load_customers()  # Refresh the combo box

    def save_bill(self):
        customer_id = self.customer_combo.currentData()
        bill_date = self.bill_date_input.date().toString("yyyy-MM-dd")
        product_name = self.product_input.text()
        total_amount = self.total_amount_input.text()

        if not customer_id:
            QMessageBox.warning(self, "Warning", "Please select a customer.")
            return

        sql = "INSERT INTO bills (customer_id, bill_date, product_name, total_amount) VALUES (%s, %s, %s, %s)"
        val = (customer_id, bill_date, product_name, total_amount)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        QMessageBox.information(self, "Success", "Bill saved successfully.")
        self.clear_inputs()

    def view_customers(self):
        self.mycursor.execute("SELECT * FROM customers")
        results = self.mycursor.fetchall()

        self.customers_table.setRowCount(len(results))
        self.customers_table.setColumnCount(len(results[0]))
        self.customers_table.setHorizontalHeaderLabels(["ID", "Name", "Address", "Phone"])

        for row_index, row_data in enumerate(results):
            for col_index, cell_data in enumerate(row_data):
                self.customers_table.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))

    def view_bills(self):
        self.mycursor.execute("SELECT * FROM bills")
        results = self.mycursor.fetchall()

        self.bills_table.setRowCount(len(results))
        self.bills_table.setColumnCount(len(results[0]))
        self.bills_table.setHorizontalHeaderLabels(["ID", "Customer ID", "Bill Date", "Product Name", "Total Amount"])

        for row_index, row_data in enumerate(results):
            for col_index, cell_data in enumerate(row_data):
                self.bills_table.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))

    def clear_inputs(self):
        self.name_input.clear()
        self.address_input.clear()
        self.phone_input.clear()
        self.total_amount_input.clear()
        self.product_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
