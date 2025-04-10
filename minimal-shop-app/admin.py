# admin_app.py
import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit,
    QPushButton, QMessageBox, QVBoxLayout, QLabel, QInputDialog
)

# --- CONFIGURATIONS ---
ADMIN_PASSWORD = "admin123"  # Change this to your preferred password
DB_PATH = "shop.db"

class AdminApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin - Add Goods")

        layout = QVBoxLayout()

        # -- Form to Add Goods
        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.color_input = QLineEdit()
        self.size_input = QLineEdit()
        self.type_input = QLineEdit()
        self.price_input = QLineEdit()

        self.form_layout.addRow("Name:", self.name_input)
        self.form_layout.addRow("Color:", self.color_input)
        self.form_layout.addRow("Size:", self.size_input)
        self.form_layout.addRow("Type:", self.type_input)
        self.form_layout.addRow("Price:", self.price_input)

        layout.addLayout(self.form_layout)

     
        self.add_button = QPushButton("Add Good")
        self.add_button.clicked.connect(self.add_good)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_good(self):
        name = self.name_input.text().strip()
        color = self.color_input.text().strip()
        size = self.size_input.text().strip()
        type_ = self.type_input.text().strip()
        try:
            price = float(self.price_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Price must be a number.")
            return

        if not name:
            QMessageBox.warning(self, "Missing Info", "Name is required.")
            return

        conn = sqlite3.connect(DB_PATH)
        
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS goods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                color TEXT NOT NULL,
                size TEXT NOT NULL,
                type TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        c.execute('''
            INSERT INTO goods (name, color, size, type, price)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, color, size, type_, price))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Good added successfully.")

        self.name_input.clear()
        self.color_input.clear()
        self.size_input.clear()
        self.type_input.clear()
        self.price_input.clear()

def request_admin_password():
    password, ok = QInputDialog.getText(None, "Admin Login", "Enter Admin Password:")
    return password if ok else None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # -- Password Protection
    password = request_admin_password()
    if password != ADMIN_PASSWORD:
        QMessageBox.critical(None, "Access Denied", "Incorrect password. Exiting.")
        sys.exit()

    window = AdminApp()
    window.resize(400, 250)
    window.show()

    sys.exit(app.exec())
