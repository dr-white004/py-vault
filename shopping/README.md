# 🛒 Minimalist Offline Goods Ordering System (PySide6 + SQLite)

This is a lightweight **offline desktop app** with two roles — **Admin** and **User** — designed for simple inventory management and order generation **without constant internet access**.

---

## ⚙️ Technologies Used

- **Python 3.x** – Core language (must be pre-installed)
- **PySide6** – GUI library for both admin and user interface
- **SQLite** – Embedded database engine (no separate setup needed)
- **PyInstaller** – Used to package the user app into a standalone executable

---

## 🛠️ How It Works

### 1. **Admin App (`admin_app.py`)**

The admin:
- Logs in using a password prompt
- Adds goods with details (name, color, size, type, and price)
- Automatically stores all entries in a local database (`shop.db`)

> ✅ You **must run the admin app at least once** to populate the database before distributing the user app.

---

### 2. **User App (`dist/` folder)**

Packaged with **PyInstaller**, the user app allows anyone to:
- Browse available goods
- Filter based on attributes
- Select desired items
- Enter their phone number
- Generate a printable/downloadable **invoice** as a text file

> 📝 This invoice can be emailed or shared back with the admin using any method (manual, online, Bluetooth, etc.)

> ⚠️ **Important:** Ensure `shop.db` (created by the admin app) is in the **same directory** as the user app executable.

---

## ✅ Getting Started (For Developers or Admins)

### Prerequisites
- Python 3.x installed on your system
- Internet access (just once) to install dependencies

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

# 2. Create a virtual environment (recommended)
python -m venv shopenv
shopenv\Scripts\activate  # On Windows
# source shopenv/bin/activate  # On macOS/Linux

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Launch the Admin App
python admin_app.py
