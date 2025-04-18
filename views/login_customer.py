
# Import necessary modules
import tkinter as tk 
from tkinter import messagebox
from PIL import ImageTk
from customer_datbase import create_database, check_credentials_customer

#----------------------------------------------- Create a class for the customer login app --------------------------------------------------#
class CustomerLoginApp: 
    def __init__(self, root):
        self.root = root
        self.root.geometry("990x660+50+50")                         # Set the size of the window
        self.root.resizable(0, 0)                                   # Prevent the window from being resized
        self.root.title("Customer Login Page")                      # Set the title of the window
        self.root.configure(bg="#f8f9fa")                           # Set the background color of the window

        # Ensure database is created
        create_database()

#------------------------------------------------- Background Image ------------------------------------------------------------------------#
        bgImage = ImageTk.PhotoImage(file="./image/background img.png")     # Load the background image
        bgLabel = tk.Label(self.root, image=bgImage)                        # Create a label to display the background image
        bgLabel.place(x=0, y=0)                                             # Place the label at the top left corner of the window
        self.bgImage = bgImage                                              # Store the background image

        # UI Elements
        self.create_ui()

#============================================= Create the UI elements for the login page =======================================================#
    def create_ui(self):
        heading = tk.Label(self.root, text="Welcome to Customer Login", font=("Aptos Black", 16, "bold"), bg="white", fg="#FFC107") 
        heading.place(x=570, y=100)

#create the email entry field
        self.email_entry = self.create_entry(550, 200, "Email") 
# create the password entry field
        self.password_entry = self.create_entry(550, 290, "Password", is_password=True) 

# create the login button
        tk.Button( 
            self.root, text="Login", font=("Aptos Black", 14, "bold"), fg="white", bg="#0275d8", cursor="hand2",
            bd=0, width=19, command=self.login_user
        ).place(x=600, y=365)

# create the OR Label
        tk.Label(
            self.root, text="----------------------------OR----------------------------",
            font=("Aptos Black", 12, "bold"), fg="#FFC107", bg="white"
        ).place(x=565, y=420)

# create the sign up button
        tk.Button(
            self.root, text="Create as a Customer", font=("Aptos Black", 12, "bold underline"), fg="#0275d8", cursor="hand2",
            bd=0, width=19, command=self.register_user
        ).place(x=620, y=490)
# Cewate the back button
        tk.Button(
            self.root, text="Back", font=("Aptos Black", 12, "bold"), fg="white", bg="#d9534f", cursor="hand2",
            bd=0, width=10, command=self.go_back
        ).place(x=20, y=20)

    # Create an entry field with a placeholder
    def create_entry(self, x, y, placeholder, is_password=False):
        entry = tk.Entry(self.root, width=25, font=("Aptos Black", 12), bd=0, fg="gray", show="*" if is_password else None)
        entry.place(x=x, y=y)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: self.clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda e: self.reset_placeholder(entry, placeholder))
        tk.Frame(self.root, width=325, height=2, bg="#0275d8").place(x=x, y=y+25)
        return entry

    # Clear the placeholder text when the entry field is focused
    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")

    # Reset the placeholder text when the entry field is unfocused
    def reset_placeholder(self, entry, placeholder):   
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    # Check the user's credentials and log them in if they are correct
    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or email == "Email":
            messagebox.showerror("Error", "Please enter your email.")
            return
        if not password or password == "Password":
            messagebox.showerror("Error", "Please enter your password.")
            return

        if check_credentials_customer(email, password):
            messagebox.showinfo("Success", "Login successful!")
            # Redirect to the customer dashboard
            import customer_dashboard
            self.new_window = tk.Toplevel(self.root)
            customer_dashboard.CustomerDashboardApp(self.new_window)
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    # Redirect the user to the customer registration page
    def register_user(self):
        self.root.destroy()
        import signup_customer
        signup_customer.signupCustomerApp(tk.Tk())

    # Close the login page
    def go_back(self):
        """Closes the current window and reopens the main login page (main.py)."""
        self.root.destroy()
        import main  # Import the main.py file, which is your entry point
        main.main()  # Assuming main.py has a main() function to initialize the app

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    CustomerLoginApp(root)
    root.mainloop()
