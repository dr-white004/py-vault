import sys
import os
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QCheckBox, QLineEdit, QPushButton, QMessageBox, QLabel
)

DB_PATH = "shop.db"
INVOICE_FOLDER = "invoices"

#  invoice folder must exist first
os.makedirs(INVOICE_FOLDER, exist_ok=True)

class UserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shop - Buy Goods")
        self.setMinimumWidth(700)

        self.layout = QVBoxLayout()
        self.instructions = QLabel("Select the items you want to buy:")
        self.layout.addWidget(self.instructions)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Select", "Name", "Color", "Size", "Type", "Price"])
        self.layout.addWidget(self.table)

        self.load_goods()

        # --- Phone number input ---
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        self.layout.addWidget(self.phone_input)

        # --- Buy Button ---
        self.buy_button = QPushButton("Buy Selected Items")
        self.buy_button.clicked.connect(self.generate_invoice)
        self.layout.addWidget(self.buy_button)

        self.setLayout(self.layout)

    def load_goods(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, name, color, size, type, price FROM goods")
        goods = c.fetchall()
        conn.close()

        self.table.setRowCount(len(goods))

        for row_idx, (id_, name, color, size, type_, price) in enumerate(goods):
            checkbox = QCheckBox()
            self.table.setCellWidget(row_idx, 0, checkbox)
            self.table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(color or ""))
            self.table.setItem(row_idx, 3, QTableWidgetItem(size or ""))
            self.table.setItem(row_idx, 4, QTableWidgetItem(type_ or ""))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"${price:.2f}"))

    def generate_invoice(self):
        selected_items = []
        total_price = 0.0

        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                name = self.table.item(row, 1).text()
                color = self.table.item(row, 2).text()
                size = self.table.item(row, 3).text()
                type_ = self.table.item(row, 4).text()
                price_str = self.table.item(row, 5).text().replace("$", "")
                price = float(price_str)
                total_price += price
                selected_items.append((name, color, size, type_, price))

        if not selected_items:
            QMessageBox.warning(self, "No Items", "Please select at least one item.")
            return

        phone = self.phone_input.text().strip()
        if not phone:
            QMessageBox.warning(self, "Missing Info", "Please enter your phone number.")
            return

        # Generate invoice content
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        invoice_name = f"invoice_{phone}_{timestamp}.txt"
        user_invoice_path = os.path.join(os.getcwd(), invoice_name)
        admin_invoice_path = os.path.join(INVOICE_FOLDER, invoice_name)

        invoice_lines = [
            "INVOICE",
            f"Phone Number: {phone}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "-" * 40
        ]

        for item in selected_items:
            line = f"Name: {item[0]}, Color: {item[1]}, Size: {item[2]}, Type: {item[3]}, Price: ${item[4]:.2f}"
            invoice_lines.append(line)

        invoice_lines.append("-" * 40)
        invoice_lines.append(f"TOTAL: ${total_price:.2f}")
        invoice_content = "\n".join(invoice_lines)

        # Save two copies of the invoice
        with open(user_invoice_path, "w") as f:
            f.write(invoice_content)
        with open(admin_invoice_path, "w") as f:
            f.write(invoice_content)

        QMessageBox.information(self, "Purchase Complete", f"Invoice saved as:\n{invoice_name}")
        self.phone_input.clear()

      
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserApp()
    window.show()
    sys.exit(app.exec())
