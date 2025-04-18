import sqlite3

# Function to create the database and Driver table
def create_database():
    conn = sqlite3.connect('taxi_booking.db')
    cursor = conn.cursor()

    # Create Driver database table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Driver (
            Driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Driver_Full_Name TEXT NOT NULL,
            Driver_License_Number TEXT NOT NULL UNIQUE,
            Driver_Vehicle_Number TEXT NOT NULL UNIQUE,
            Driver_Phone_Number TEXT NOT NULL UNIQUE,
            Driver_Email TEXT NOT NULL UNIQUE,
            Driver_Password TEXT NOT NULL
        )
    ''')
    print('Driver Table created successfully.')
    conn.commit()
    conn.close()

# Function to insert data into Driver table
def insert_record_driver(Driver_Full_Name, Driver_License_Number, Driver_Vehicle_Number, Driver_Phone_Number, Driver_Email, Driver_Password):
    try:
        conn = sqlite3.connect('taxi_booking.db')
        cursor = conn.cursor()
        query = """
            INSERT INTO Driver 
            (Driver_Full_Name, Driver_License_Number, Driver_Vehicle_Number, Driver_Phone_Number, Driver_Email, Driver_Password) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (Driver_Full_Name, Driver_License_Number, Driver_Vehicle_Number, Driver_Phone_Number, Driver_Email, Driver_Password))
        conn.commit()
        print("Record inserted successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")  # Catching unique constraint violations
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

# Function to retrieve all records (e.g., for driver login)
def check_credentials_driver(Driver_Email, Driver_Password):
    try:
        conn = sqlite3.connect('taxi_booking.db')
        cursor = conn.cursor()
        query = """
            SELECT Driver_id 
            FROM Driver 
            WHERE Driver_Email = ? AND Driver_Password = ?
        """
        cursor.execute(query, (Driver_Email, Driver_Password))
        result = cursor.fetchone()
        if result:
            print("Login successful!")
        else:
            print("Invalid credentials.")
        return result
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None
    finally:
        conn.close()
