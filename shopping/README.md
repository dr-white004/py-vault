# Minimalist Offline Goods Ordering System (PySide6 + SQLite)

This is a lightweight offline desktop app split into two roles — **Admin** and **User** — designed for managing and requesting goods without requiring full-time internet access.

## 🛠 Technologies Used
- **PySide6 (Qt for Python)** – for the GUI
- **SQLite** – for local database storage
- **PyInstaller** – for packaging user app as a standalone executable

---

## 📦 How It Works

### 1. **Admin App (`admin_app.py`)**
The admin is responsible for:
- Logging in with a secure password
- Adding available goods (with attributes like name, color, size, type, and price)
- Managing the goods list stored in a local SQLite database (`shop.db`)

> ⚠️ You must run the admin app at least once to populate the goods.

---

### 2. **User App (Packaged Executable)**
Users:
- Open the packaged app from the `dist/` folder
- Select from the list of goods (filtered by attributes)
- Enter their phone number
- Generate an invoice with all selected items

The invoice is:
- Saved locally as a text file
- Intended to be sent to the admin (via email or other methods)

> ⚠️ The shop.db app generated after running the admin app atleast once must be in the same directory as the bunduled user app for it to work properly
---

## 📄 Example Use Case

> A small rural retail store without stable internet can install the admin app on the owner's laptop to add inventory. The packaged user app can be shared via USB or memory card with local agents or customers. They make selections and generate an invoice offline, which is later sent to the admin once internet is available.

---

## 💡 Minimal Internet Usage

The only feature planned to require internet is **emailing the invoice** back to the admin — the rest of the system works **fully offline**.

---

##  Getting Started 

1. Clone the repo
2. Run the setup script below to initialize the database:

```bash
python admin.py
