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
* **Frontend:** HTML, CSS, JS, Bootstrap  
* **Database:** MySQL  
* **Connector:** mysql-connector-python  

---

## 📁 Project Structure

```

project/
│── app.py
│── db_config.py
│── requirements.txt
│── README.md
│── database/
│   └── rehabcare_db.sql
│── templates/
│── static/

````

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd project
````

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

### 5️⃣ Database Setup

Database dump is provided in the `database/` folder.

```bash
# Create database
mysql -u root -p
CREATE DATABASE rehabcare_db;

# Import dump
mysql -u root -p rehabcare_db < database/rehabcare_db.sql
```

Make sure MySQL service is running before importing.

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

* Session-based authentication is used
* Debug mode enabled (disable in production)
* Ensure MySQL service is running

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

