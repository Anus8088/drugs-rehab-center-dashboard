import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ansari8088',
    'database': 'rehab_center_db'  # Updated database name
}

def get_db_connection():
    """
    Establishes and returns a MySQL database connection
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as err:
        print(f"Database Connection Error: {err}")
        return None

def test_connection():
    """
    Tests the database connection
    """
    conn = get_db_connection()
    if conn:
        print("✅ Database connection successful!")
        conn.close()
        return True
    else:
        print("❌ Database connection failed!")
        return False

if __name__ == "__main__":
    test_connection()