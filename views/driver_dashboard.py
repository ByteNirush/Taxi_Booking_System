
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from login_admin import *

# Ensure the bookings database has the correct schema
def ensure_driver_column():
    conn = sqlite3.connect("Customer_Database.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(bookings)")
    columns = [col[1] for col in cursor.fetchall()]
    if "driver" not in columns:
        cursor.execute("ALTER TABLE bookings ADD COLUMN driver TEXT DEFAULT NULL")
        conn.commit()
    conn.close()


# Function to load drivers from the taxi_booking.db database
def load_drivers_from_db():
    """Retrieve all drivers from the Driver table."""
    conn = sqlite3.connect("taxi_booking.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Driver_Full_Name FROM Driver")
    drivers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return drivers


class DriverDashboardApp:
    def __init__(self, parent, driver_id):
        self.parent = parent
        self.driver_id = driver_id
        self.root = parent
        self.root.title("Driver Dashboard")
        self.root.geometry("1200x660+50+50")
        self.root.resizable(0, 0)
        self.root.config(bg="black")

        # Create the side menu
        self.create_side_menu()

        # Create the content frame
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Load the home page
        self.go_home()

    def connect_db(self):
        """Establish a connection to the database."""
        try:
            conn = sqlite3.connect("Customer_Database.db")  # Correct database path
            return conn, conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
            return None, None

    def create_side_menu(self):
        self.side_menu = tk.Frame(self.root, bg="#343a40", width=180, height=660, padx=10, pady=10)
        self.side_menu.pack(side="left", fill="y")

        tk.Button(self.side_menu, text="Home", bg="#FFC107", font=("Arial", 12), padx=20, pady=10,
                    command=self.go_home).pack(pady=10)
        tk.Button(self.side_menu, text="Assigned Trips", bg="#FFC107", font=("Arial", 12), padx=20, pady=10,
                    command=self.view_assigned_trips).pack(pady=10)
        tk.Button(self.side_menu, text="Past Trips", bg="#FFC107", font=("Arial", 12), padx=20, pady=10,
                    command=self.view_past_trips).pack(pady=10)
        tk.Button(self.side_menu, text="Log Out", bg="#FFC107", font=("Arial", 12), padx=20, pady=10,
                    command=self.logout).pack(pady=10)

    def go_home(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        try:
            original_image = Image.open("./image/driverbackgtound.jpg")
            resized_image = original_image.resize((1250, 700))
            bg_image = ImageTk.PhotoImage(resized_image)
            bg_label = tk.Label(self.content_frame, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(x=0, y=0)
        except IOError:
            messagebox.showerror("Error", "Background image not found!")
            return

        welcome_label = tk.Label(
            self.content_frame,
            text=f"Welcome to Dashboard, Driver {self.driver_id}!",
            font=("Arial", 20, "bold") )
        welcome_label.pack(pady=20)

    def view_assigned_trips(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        columns = ("Booking ID", "Pickup Location", "Drop-off Location", "Pickup Time", "Pickup Date")
        trips_table = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        for col in columns:
            trips_table.heading(col, text=col)
            trips_table.column(col, width=150, anchor="center")

        trips_table.pack(fill="both", expand=True, pady=10)

        conn, cursor = self.connect_db()
        if not conn:
            return  # Exit if connection fails

        try:
            cursor.execute("""
                SELECT id, pickup_location, dropoff_location, pickup_time, pickup_date
                FROM bookings
                WHERE driver = ?
            """, (self.driver_id,))
            trips = cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {e}")
            conn.close()
            return

        # Close the database connection
        conn.close()

        if not trips:
            messagebox.showinfo("No Trips", "No trips have been assigned to you.")
        else:
            for trip in trips:
                trips_table.insert("", tk.END, values=trip)

    def view_past_trips(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # Implement functionality as needed
        columns = ("Trip ID",
                    "Customer ID", 
                    "Pickup Location", 
                    "Drop-off Location", 
                    "Pickup Time", 
                    "Pickup Date",
                    "Status"
                    )
        customer_table = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        for col in columns:
            customer_table.heading(col, text=col)
            customer_table.column(col, width=150, anchor="center")

        # Add scrollbars
        y_scroll = ttk.Scrollbar(self.content_frame, orient="vertical", command=customer_table.yview)
        customer_table.configure(yscroll=y_scroll.set)
        y_scroll.pack(side="right", fill="y")

        customer_table.pack(fill="both", expand=True, pady=10)

    def logout(self):
        import login_driver
        self.new_window = tk.Toplevel(self.root)
        app = login_driver.DriverLoginApp(self.new_window)
        self.root.withdraw()


# Driver Dashboard Execution
if __name__ == "__main__":
    root = tk.Tk()
    driver_id = 1  # Replace this with the actual driver_id (e.g., fetched from a database)
    app = DriverDashboardApp(root, driver_id)
    root.mainloop()
