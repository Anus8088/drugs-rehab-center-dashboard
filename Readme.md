# RehabCare Pro 🏥

A complete **Rehabilitation Center Management System** built with **Flask & MySQL**.
This system helps manage patients, rooms, billing, payments, and medicine records in a centralized web application.

---

## 🚀 Features

* 🔐 User Authentication (Login / Logout)
* 🧑‍⚕️ Patient Management (Add, Edit, View)
* 🏢 Branch & Room Allocation System
* 🛏 Bed Availability Tracking
* 💳 Billing & Invoice Management
* 💰 Payment Recording & History
* 💊 Medicine Inventory & Dosage Records
* 📊 Dashboard with Statistics

---

## 🛠 Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, Jinja2, Bootstrap (assumed)
* **Database:** MySQL
* **Connector:** mysql-connector-python

---

## 📁 Project Structure (Simplified)

```
project/
│── app.py
│── db_config.py
│── requirements.txt
│── README.md
│── templates/
│── static/
│── venv/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd project
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Database

Edit **db_config.py** and add your MySQL credentials:

```python
host = "localhost"
user = "root"
password = "your_password"
database = "rehabcare_db"
```

Make sure database & tables already exist.

---

## ▶️ Run the Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## 🔐 Default Notes

* Session-based authentication
* Make sure MySQL service is running
* Debug mode enabled (disable in production)

---

## 📌 Future Improvements

* Password hashing
* Role-based access control
* PDF invoice export
* API support
* Docker deployment

---

## 👨‍💻 Developer

**Anas Ansari**
RehabCare Pro – 2025

---

⭐ If you like this project, feel free to improve or extend it!
