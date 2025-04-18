
# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import sqlite3
from PIL import Image, ImageTk


# Create a class for the Customer Dashboard App
class CustomerDashboardApp:
    def __init__(self, root):
        # Initialize the root window
        self.root = root
        self.root.title("Taxi Booking System")
        self.root.geometry("990x660+50+50")
        self.root.resizable(0, 0)

        # Set up the UI
        self.setup_ui()
        # Go to the home page
        self.go_home()

    # Set up the UI
    def setup_ui(self):
        # Create a menu frame
        self.menu_frame = tk.Frame(self.root, bg="#FFC107", width=250, height=500)
        self.menu_frame.pack(side="left", fill="y")

        # Create menu buttons
        menu_buttons = [
            ("Home", self.go_home),
            ("Book A Trip", self.book_trip),
            ("View Bookings", self.view_bookings),
            ("Log Out", self.logout),
        ]

        # Pack the menu buttons
        for text, command in menu_buttons:
            btn = tk.Button(self.menu_frame, text=text, command=command, bg="#FFC107", fg="white",
                            font=("Arial", 12, "bold"), bd=0)
            btn.pack(fill="x", padx=10, pady=10)

        # Create a content frame
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

    # Connect to the database
    @staticmethod
    def connect_db():
        conn = sqlite3.connect("Customer_Database.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pickup_location TEXT,
            dropoff_location TEXT,
            pickup_date TEXT,
            pickup_time TEXT,
            driver TEXT DEFAULT NULL
        )
        """)
        conn.commit()
        return conn, cursor

    # Go to the home page
    def go_home(self):
        # Destroy all widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        try:
            # Open the background image and resize it
            original_image = Image.open("./image/customerbackground.jpg")
            resized_image = original_image.resize((990, 660))
            bg_image = ImageTk.PhotoImage(resized_image)
            bg_label = tk.Label(self.content_frame, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(x=0, y=0)
        except IOError:
            messagebox.showerror("Error", "Background image not found!")
            
        welcome_label = tk.Label(self.content_frame, text="Welcome to Customer Dashboard", font=("Arial", 20, "bold"))
        welcome_label.pack(pady=40)

    # Book a trip
    def book_trip(self):
        # Destroy all widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create a frame for the ride
        ride_frame = tk.LabelFrame(self.content_frame, text="Customer Ride", padx=10, pady=10, font=("Arial", 12))
        ride_frame.pack(pady=30, fill="x", padx=20)

        # Create ride fields
        ride_fields = ["PickUp Location", "Drop-off Location"]
        ride_entries = {}

        # Create labels and entries for the ride fields
        for idx, field in enumerate(ride_fields):
            label = tk.Label(ride_frame, text=f"{field}:", font=("Arial", 10))
            label.grid(row=idx, column=0, sticky="e", pady=5, padx=5)

            entry = ttk.Entry(ride_frame, width=25)
            entry.grid(row=idx, column=1, pady=5)
            ride_entries[field] = entry

        # Create a label and date picker for the pickup date
        date_label = tk.Label(ride_frame, text="Pickup Date:", font=("Arial", 10))
        date_label.grid(row=len(ride_fields), column=0, sticky="e", pady=5, padx=5)

        date_picker = DateEntry(ride_frame, width=23, background="darkblue", foreground="white", borderwidth=2)
        date_picker.set_date(datetime.now().date())
        date_picker.grid(row=len(ride_fields), column=1, pady=5)

        # Create a label and time picker for the pickup time
        time_label = tk.Label(ride_frame, text="Pickup Time:", font=("Arial", 10))
        time_label.grid(row=len(ride_fields) + 1, column=0, sticky="e", pady=5, padx=5)

        start_time = datetime.strptime("06:00", "%H:%M")
        end_time = datetime.strptime("22:00", "%H:%M")
        time_values = [start_time.strftime("%H:%M")]
        while start_time < end_time:
            start_time += timedelta(minutes=30)
            time_values.append(start_time.strftime("%H:%M"))

        time_picker = ttk.Combobox(ride_frame, values=time_values, width=22, state="readonly")
        time_picker.grid(row=len(ride_fields) + 1, column=1, pady=5)
        time_picker.set(time_values[0])

        # Create a function to book the trip
        def book_now():
            details = {
                "PickUp Location": ride_entries["PickUp Location"].get().strip(),
                "Drop-off Location": ride_entries["Drop-off Location"].get().strip(),
                "Pickup Date": date_picker.get(),
                "Pickup Time": time_picker.get(),
            }

            if all(details.values()) and details["Pickup Time"] in time_values:
                conn, cursor = self.connect_db()
                cursor.execute("""
                INSERT INTO bookings (pickup_location, dropoff_location, pickup_date, pickup_time)
                VALUES (?, ?, ?, ?)
                """, (details["PickUp Location"], details["Drop-off Location"], details["Pickup Date"], details["Pickup Time"]))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", f"Trip booked successfully!\n\nDetails:\n{details}")
            else:
                messagebox.showerror("Error", "Please fill in all fields and select a valid time.")

        # Create a button to book the trip
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=20)

        book_now_button = tk.Button(button_frame, text="Book Now!", bg="#FFC107", padx=20, pady=10, font=("Arial", 10, "bold"), command=book_now)
        book_now_button.grid(row=0, column=0, padx=10)

    # View bookings
    def view_bookings(self):
        # Destroy all widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Connect to the database
        conn, cursor = self.connect_db()
        cursor.execute("SELECT * FROM bookings")
        all_bookings = cursor.fetchall()
        conn.close()

        # If there are bookings, display them
        if all_bookings:
            bookings_frame = tk.LabelFrame(self.content_frame, text="Booked Trips", padx=10, pady=10, font=("Arial", 12))
            bookings_frame.pack(pady=30, fill="x", padx=20)

            for idx, booking in enumerate(all_bookings):
                row = f"Booking {idx + 1}:"
                booking_details = f"PickUp: {booking[1]}, DropOff: {booking[2]}, Date: {booking[3]}, Time: {booking[4]}"

                tk.Label(bookings_frame, text=row, font=("Arial", 10, "bold")).grid(row=idx * 2, column=0, sticky="w", padx=10)
                tk.Label(bookings_frame, text=booking_details, font=("Arial", 10)).grid(row=idx * 2 + 1, column=0, sticky="w", padx=10)

                # Create a button to cancel the booking
                cancel_button = tk.Button(
                    bookings_frame, text="Cancel", bg="red", fg="white", font=("Arial", 10),
                    command=lambda booking_id=booking[0]: self.delete_booking(booking_id)
                )
                cancel_button.grid(row=idx * 2 + 1, column=1, padx=10)

                # Add Update button
                update_button = tk.Button(
                    bookings_frame, text="Update", bg="blue", fg="white", font=("Arial", 10),
                    command=lambda booking=booking: self.update_booking(booking)
                )
                update_button.grid(row=idx * 2 + 1, column=2, padx=10)
        else:
            messagebox.showinfo("No Bookings", "No bookings have been made yet.")

    # Delete a booking
    def delete_booking(self, booking_id):
        # Connect to the database
        conn, cursor = self.connect_db()
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Booking canceled successfully!")
        self.view_bookings()

    # Update a booking
    def update_booking(self, booking):
        start_time = datetime.strptime("06:00", "%H:%M")
        end_time = datetime.strptime("22:00", "%H:%M")
        time_values = []

        while start_time <= end_time:
            time_values.append(start_time.strftime("%H:%M"))
            start_time += timedelta(minutes=30)

        # Destroy all widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create a frame for the ride
        ride_frame = tk.LabelFrame(self.content_frame, text="Update Booking", padx=10, pady=10, font=("Arial", 12))
        ride_frame.pack(pady=30, fill="x", padx=20)

        fields = ["PickUp Location", "Drop-off Location", "Pickup Date", "Pickup Time"]
        values = [booking[1], booking[2], booking[3], booking[4]]
        entries = {}

        # Create labels and entries for the ride fields
        for idx, field in enumerate(fields[:-2]):
            label = tk.Label(ride_frame, text=f"{field}:", font=("Arial", 10))
            label.grid(row=idx, column=0, sticky="e", pady=5, padx=5)

            entry = ttk.Entry(ride_frame, width=25)
            entry.insert(0, values[idx])
            entry.grid(row=idx, column=1, pady=5)
            entries[field] = entry

        # Create a label and date picker for the pickup date
        date_label = tk.Label(ride_frame, text="Pickup Date:", font=("Arial", 10))
        date_label.grid(row=2, column=0, sticky="e", pady=5, padx=5)
        date_picker = DateEntry(ride_frame, width=23, background="darkblue", foreground="white", borderwidth=2)
        date_picker.set_date(values[2])
        date_picker.grid(row=2, column=1, pady=5)

        # Create a label and time picker for the pickup time
        time_label = tk.Label(ride_frame, text="Pickup Time:", font=("Arial", 10))
        time_label.grid(row=3, column=0, sticky="e", pady=5, padx=5)

        time_picker = ttk.Combobox(ride_frame, values=time_values, width=22, state="readonly")
        time_picker.set(values[3])  # Set the default time
        time_picker.grid(row=3, column=1, pady=5)

        # Create a function to update the booking
        def update_details():
            details = {
                "PickUp Location": entries["PickUp Location"].get().strip(),
                "Drop-off Location": entries["Drop-off Location"].get().strip(),
                "Pickup Date": date_picker.get(),
                "Pickup Time": time_picker.get(),
            }

            if all(details.values()) and details["Pickup Time"] in time_values:
                conn, cursor = self.connect_db()
                cursor.execute("""
                    UPDATE bookings 
                    SET pickup_location = ?, dropoff_location = ?, pickup_date = ?, pickup_time = ?
                    WHERE id = ?
                """, (details["PickUp Location"], details["Drop-off Location"], details["Pickup Date"], details["Pickup Time"], booking[0]))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Booking updated successfully!")
                self.view_bookings()
            else:
                messagebox.showerror("Error", "Please fill in all fields and select a valid time.")

        # Create a button to update the booking
        update_button = tk.Button(ride_frame, text="Update Booking", bg="#FFC107", fg="#343a40", font=("Arial", 12), command=update_details)
        update_button.grid(row=4, column=1, pady=10)

    # Log out
    def logout(self):
        # Import the login_customer module
        import login_customer
        # Create a new window
        self.new_window = tk.Toplevel(self.root)
        # Create a new instance of the CustomerLoginApp class
        app = login_customer.CustomerLoginApp(self.new_window)
        self.root.withdraw()


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerDashboardApp(root)
    root.mainloop()
