
from tkinter import messagebox
import tkinter as tk
from PIL import ImageTk
from customer_datbase import create_database, insert_record_customer

class signupCustomerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("990x660+50+50")
        self.root.resizable(0, 0)
        self.root.title("Taxi Booking Registration Page")
        self.root.configure(bg="#f8f9fa")

        # Ensure database is created
        create_database()

        # Background Image
        bgImage = ImageTk.PhotoImage(file="./image/background img.png")
        bgLabel = tk.Label(self.root, image=bgImage)
        bgLabel.place(x=0, y=0)
        self.bgImage = bgImage  # Prevent garbage collection

        # UI Elements
        self.create_ui()

    def create_ui(self):
        heading = tk.Label(
            self.root, text="Register For Customer", font=("Aptos Black", 16, "bold"), bg="white", fg="#FFC107"
        )
        heading.place(x=600, y=80)

        # Name Entry
        self.name_entry = self.create_entry(550, 150, "Full Name")
        # Address Entry
        self.address_entry = self.create_entry(550, 225, "Address")
        # Phone Entry
        self.phone_entry = self.create_entry(550, 300, "Phone Number", validate=True)
        # Email Entry
        self.email_entry = self.create_entry(550, 375, "Email")
        # Password Entry
        self.password_entry = self.create_entry(550, 450, "Password", is_password=True)

        # Register Button
        tk.Button(
            self.root, text="Register", font=("Aptos Black", 14, "bold"), fg="white", bg="#0275d8", cursor="hand2",
            bd=0, width=15, command=self.register_user
        ).place(x=635, y=525)

        # Back Button
        tk.Button(
            self.root, text="Back", font=("Aptos Black", 12, "bold"), fg="white", bg="#d9534f", cursor="hand2",
            bd=0, width=10, command=self.go_back
        ).place(x=20, y=20)

    def create_entry(self, x, y, placeholder, validate=False, is_password=False):
        entry = tk.Entry(self.root, width=25, font=("Aptos Black", 12), bd=0, fg="gray", show="*" if is_password else None)
        entry.place(x=x, y=y)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: self.clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda e: self.reset_placeholder(entry, placeholder))
        if validate:
            entry.bind("<KeyRelease>", lambda e: self.validate_number(entry))
        tk.Frame(self.root, width=325, height=2, bg="#0275d8").place(x=x, y=y+25)
        return entry

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")

    def reset_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    def validate_number(self, entry):
        if not entry.get().isdigit() and entry.get() != "":
            entry.config(fg="red")
        else:
            entry.config(fg="black")

    def register_user(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if any(field in ["", "Full Name", "Address", "Phone Number", "Email", "Password"] for field in [name, address, phone, email, password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not phone.isdigit():
            messagebox.showerror("Error", "Phone number must contain only digits.")
            return

        try:
            insert_record_customer(name, address, phone, email, password)
            messagebox.showinfo("Success", "Account created successfully!")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {e}")

    def go_back(self):
        self.root.destroy()
        import login_customer
        login_customer.CustomerLoginApp(tk.Tk())

if __name__ == "__main__":
    root = tk.Tk()
    signupCustomerApp(root)
    root.mainloop()
