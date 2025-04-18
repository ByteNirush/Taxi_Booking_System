import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import sys
from driver_database import create_database, insert_record_driver

class signupDriverApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("990x660+50+50")
        self.root.resizable(0, 0)
        self.root.title("Taxi Booking Registration Page")
        self.root.configure(bg="#f8f9fa")

        # Background Image
        bgImage = ImageTk.PhotoImage(file="./image/background img.png")
        bgLabel = tk.Label(self.root, image=bgImage)
        bgLabel.place(x=0, y=0)
        self.bgImage = bgImage  # Prevent garbage collection

        # Create UI elements
        self.create_ui()

    def create_ui(self):
        """Creates the registration UI."""
        heading = tk.Label(
            self.root, text="Register For Driver", font=("Aptos Black", 16, "bold"), bg="white", fg="#FFC107"
        )
        heading.place(x=610, y=80)

        # Name Entry
        self.name_entry = self.create_entry(550, 150, "Full Name")

        # License Number Entry
        self.license_entry = self.create_entry(550, 225, "License Number", validate_func=self.validate_number)

        # Vehicle Number Entry
        self.vehicle_number_entry = self.create_entry(550, 300, "Vehicle Number", validate_func=self.validate_number)

        # Phone Number Entry
        self.phone_entry = self.create_entry(550, 375, "Phone Number", validate_func=self.validate_number)

        # Email Entry
        self.email_entry = self.create_entry(550, 450, "Email")

        # Password Entry
        self.password_entry = self.create_entry(550, 525, "Password", show="*")

        # Register Button
        registerButton = tk.Button(
            self.root,
            text="Register",
            font=("Aptos Black", 14, "bold"), fg="white", bg="#0275d8", cursor="hand2",
            bd=0, width=15, command=self.register_user
        )
        registerButton.place(x=630, y=580)

        # Back Button
        backButton = tk.Button(
            self.root,
            text="Back",
            font=("Aptos Black", 12, "bold"), fg="white", bg="#d9534f", activeforeground="white", activebackground="#c9302c", cursor="hand2",
            bd=0, width=10, command=self.go_back,
        )
        backButton.place(x=20, y=20)

    def create_entry(self, x, y, placeholder, show=None, validate_func=None):
        entry = tk.Entry(self.root, width=25, font=("Aptos Black", 12), bd=0, fg="gray", show=show)
        entry.place(x=x, y=y)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", self.user_enter)
        entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, entry, placeholder))
        if validate_func:
            entry.bind("<KeyRelease>", lambda e: validate_func(entry))
        tk.Frame(self.root, width=325, height=2, bg="#0275d8").place(x=x, y=y + 25)
        return entry

    def user_enter(self, event):
        """Clears placeholder text when the user clicks on the entry widget.""" 
        if event.widget.get() in ["Full Name", "License Number", "Vehicle Number", "Phone Number", "Email", "Password"]:
            event.widget.delete(0, "end")
        event.widget.config(fg="black")

    def reset_placeholder(self, event, entry, placeholder):
        """Handles placeholder text when the entry widget is empty.""" 
        if not entry.get() or entry.get() == placeholder:
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    def validate_number(self, entry):
        """Validates if the input is a number for fields like License Number and Vehicle Number.""" 
        text = entry.get()
        if not text.isdigit() and text != "":
            entry.config(fg="red")
        else:
            entry.config(fg="black")

    def register_user(self):
        """Handles user registration logic.""" 
        name = self.name_entry.get()
        license_number = self.license_entry.get()
        vehicle_number = self.vehicle_number_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Simple validation for empty fields
        if any(field == "" or field in ["Full Name", "License Number", "Vehicle Number", "Phone Number", "Email", "Password"] 
            for field in [name, license_number, vehicle_number, phone, email, password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Validate fields
        if not license_number.isdigit():
            messagebox.showerror("Error", "License number should contain only numbers.")
            return

        if not vehicle_number.isdigit():
            messagebox.showerror("Error", "Vehicle number should contain only numbers.")
            return

        if not phone.isdigit():
            messagebox.showerror("Error", "Phone number should contain only numbers.")
            return
        
        try:
            insert_record_driver(name, license_number, vehicle_number, phone, email, password)
            messagebox.showinfo("Success", "Registration successful!")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {e}")
            

    def go_back(self):
        ...
        
if __name__ == "__main__":
    root = tk.Tk()
    app = signupDriverApp(root)
    root.mainloop()
