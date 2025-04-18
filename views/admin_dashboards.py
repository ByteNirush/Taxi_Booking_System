import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from login_admin import*


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


class AdminDashboardApp:
    def __init__(self, root, bookings, customers, drivers):
        self.root = root
        self.bookings = bookings  # Booking data (dynamically updated)
        self.drivers = load_drivers_from_db()  # Fetch drivers dynamically from the database
        self.customers = customers  # Customer data (passed dynamically)
        self.driver_id = None  # Driver ID (passed dynamically)

        root.title("Administrator Dashboard")
        root.geometry("1200x700+50+50")
        root.resizable(0, 0)
        root.config(bg="white")

        # Create the side menu
        self.create_side_menu()

        # Create the content frame
        self.content_frame = tk.Frame(root, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Load the home page
        self.go_home()

    def create_side_menu(self):
        self.side_menu = tk.Frame(self.root, bg="#343a40", width=180, height=700, padx=10, pady=10)
        self.side_menu.pack(side="left", fill="y")

        tk.Button(self.side_menu, text="Home", bg="#FFC107", font=("Aptos Black", 12), padx=20, pady=10, command=self.go_home).pack(pady=10)
        tk.Button(self.side_menu, text="Assign Drivers", bg="#FFC107", font=("Aptos Black", 12), padx=20, pady=10, command=self.assign_driver_window).pack(pady=10)
        tk.Button(self.side_menu, text="Customer Details", bg="#FFC107", font=("Aptos Black", 12), padx=20, pady=10, command=self.view_customer_details).pack(pady=10)
        tk.Button(self.side_menu, text="Driver Details", bg="#FFC107", font=("Aptos Black", 12), padx=20, pady=10, command=self.view_driver_details).pack(pady=10)
        tk.Button(self.side_menu, text="Log Out", bg="#FFC107", font=("Aptos Black", 12), padx=20, pady=10, command=self.logout).pack(pady=10)

    def go_home(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        try:
            original_image = Image.open("./image/taxi.jpg")
            resized_image = original_image.resize((1250, 700))
            bg_image = ImageTk.PhotoImage(resized_image)
            bg_label = tk.Label(self.content_frame, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(x=0, y=0)
        except IOError:
            messagebox.showerror("Error", "Background image not found!")
            return

        welcome_label = tk.Label(self.content_frame, text="Welcome to Admin Dashboard", font=("Arial", 20, "bold"))
        welcome_label.pack(pady=40)

    def load_bookings_from_db(self):
        """Fetch bookings from the database."""
        conn = sqlite3.connect("Customer_Database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, pickup_location, dropoff_location, pickup_date, pickup_time, driver FROM bookings")
        bookings = [
            {
                "booking_id": row[0],
                "pickup_location": row[1],
                "dropoff_location": row[2],
                "pickup_time": f"{row[3]} {row[4]}",
                "driver": row[5],
            }
            for row in cursor.fetchall()
        ]
        conn.close()
        return bookings

    def assign_driver_window(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Fetch updated bookings
        self.bookings = self.load_bookings_from_db()

        # Table for bookings
        columns = (
            "Booking ID",
            "Pickup Location",
            "Dropoff Location",
            "Pickup Time",
            "Driver",
        )
        booking_table = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            booking_table.heading(col, text=col)
            booking_table.column(col, width=150, anchor="center")
        booking_table.pack(fill="both", expand=True, pady=10)

        for booking in self.bookings:
            booking_table.insert(
                "",
                tk.END,
                values=(
                    booking["booking_id"],
                    booking["pickup_location"],
                    booking["dropoff_location"],
                    booking["pickup_time"],
                    booking["driver"] or "Unassigned",
                ),
            )

        assign_frame = tk.Frame(self.content_frame, bg="white")
        assign_frame.pack(fill="x", pady=10)

        tk.Label(assign_frame, text="Booking ID:", font=("Aptos Black", 12), bg="white").grid(row=0, column=0, padx=10, pady=5)
        booking_id_var = tk.StringVar()
        booking_id_entry = ttk.Entry(assign_frame, textvariable=booking_id_var, width=10)
        booking_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(assign_frame, text="Driver:", font=("Aptos Black", 12), bg="white").grid(row=0, column=2, padx=10, pady=5)
        driver_var = tk.StringVar()
        driver_dropdown = ttk.Combobox(assign_frame, textvariable=driver_var, values=self.drivers, state="readonly", width=15)
        driver_dropdown.grid(row=0, column=3, padx=10, pady=5)

        def refresh_booking_table():
            """Refresh the booking table after driver assignment."""
            for row in booking_table.get_children():
                booking_table.delete(row)
            for booking in self.bookings:
                booking_table.insert(
                    "",
                    tk.END,
                    values=(
                        booking["booking_id"],
                        booking["pickup_location"],
                        booking["dropoff_location"],
                        booking["pickup_time"],
                        booking["driver"] or "Unassigned",
                    ),
                )

        def assign_driver():
            booking_id = booking_id_var.get()
            selected_driver = driver_var.get()

            if not booking_id or not selected_driver:
                messagebox.showerror("Error", "Please select a booking and driver.")
                return

            conn = sqlite3.connect("Customer_Database.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE bookings SET driver = ? WHERE id = ?
            """, (selected_driver, booking_id))
            conn.commit()
            conn.close()

            # Refresh bookings from the database
            self.bookings = self.load_bookings_from_db()
            refresh_booking_table()

            messagebox.showinfo("Success", f"Driver {selected_driver} assigned to Booking ID {booking_id}.")

        assign_button = tk.Button(assign_frame, text="Assign Driver", bg="#FFC107", font=("Aptos Black", 12), command=assign_driver)
        assign_button.grid(row=0, column=4, padx=10, pady=5)

    def view_customer_details(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create a table for customer details
        columns = (
            "Customer ID",
            "Full Name",
            "Address",
            "Phone Number",
            "Email",
        )
        customer_table = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            customer_table.heading(col, text=col)
            customer_table.column(col, width=200, anchor="center")
        customer_table.pack(fill="both", expand=True, pady=10)

        # Fetch customer data from the database
        conn = sqlite3.connect("taxi_booking.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Customer_id, Customer_Full_Name, Customer_Address, Customer_Phone_Number, Customer_Email FROM Customer")
        customers = cursor.fetchall()
        conn.close()

        # Insert customer data into the table
        for customer in customers:
            customer_table.insert("", tk.END, values=customer)


    def view_driver_details(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create a table for driver details
        columns = (
            "Driver ID",
            "Full Name",
            "License Number",
            "Vehicle Number",
            "Phone Number",
            "Email",
        )
        driver_table = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            driver_table.heading(col, text=col)
            driver_table.column(col, width=200, anchor="center")
        driver_table.pack(fill="both", expand=True, pady=10)

        # Fetch driver data from the database
        conn = sqlite3.connect("taxi_booking.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Driver_id, Driver_Full_Name, Driver_License_Number, Driver_Vehicle_Number, Driver_Phone_Number, Driver_Email FROM Driver")
        drivers = cursor.fetchall()
        conn.close()

        # Insert driver data into the table
        for driver in drivers:
            driver_table.insert("", tk.END, values=driver)

    def logout(self):
        """Log out the admin and navigate back to the Admin Login page."""
        self.root.destroy()                         # Close the current Admin Dashboard window
        import login_admin                          # Import the login_admin module
        root = tk.Tk()                              # Create a new Tkinter root window
        app = login_admin.AdminLoginApp(root)       # Initialize the AdminLoginApp
        root.mainloop()                             # Start the Tkinter event loop


# Ensure the database schema is correct before starting the app
ensure_driver_column()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    drives = load_drivers_from_db()
    app = AdminDashboardApp(root, bookings=[], customers=[], drivers=[])  # Initialize the AdminDashboardApp
    root.mainloop()

