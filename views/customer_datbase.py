
import sqlite3

# Function to create the database and Customer table
def create_database():
    conn = sqlite3.connect('taxi_booking.db')
    cursor = conn.cursor()

    # Create Customer database table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customer (
                Customer_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                Customer_Full_Name TEXT NOT NULL,
                Customer_Address TEXT NOT NULL,
                Customer_Phone_Number TEXT NOT NULL UNIQUE,
                Customer_Email TEXT NOT NULL UNIQUE,
                Customer_Password TEXT NOT NULL
                )''')
    print('Customer Table created successfully.')
    conn.commit()
    conn.close()

# Function to insert a record into the Customer table
def insert_record_customer(Customer_Full_Name, Customer_Address, Customer_Phone_Number, Customer_Email, Customer_Password):
    try:
        conn = sqlite3.connect('taxi_booking.db')
        cursor = conn.cursor()
        query = """INSERT INTO Customer (Customer_Full_Name, Customer_Address, Customer_Phone_Number, Customer_Email, Customer_Password) 
                VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(query, (Customer_Full_Name, Customer_Address, Customer_Phone_Number, Customer_Email, Customer_Password))
        conn.commit()
        print('Record inserted successfully.')
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Function to retrieve a record for customer login
def check_credentials_customer(Customer_Email, Customer_Password):
    try:
        conn = sqlite3.connect('taxi_booking.db')
        cursor = conn.cursor()
        query = """SELECT Customer_id FROM Customer WHERE Customer_Email = ? AND Customer_Password = ?"""
        cursor.execute(query, (Customer_Email, Customer_Password))
        result = cursor.fetchone()
        return result
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()
