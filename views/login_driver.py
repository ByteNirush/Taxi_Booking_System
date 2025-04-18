import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from driver_database import create_database, check_credentials_driver

#================================================= Creating a TaxiBookingApp ==========================================================#

class DriverLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("990x660+50+50")
        self.root.resizable(0, 0)
        self.root.title("Driver Login Page")
        self.root.configure(bg="#f8f9fa")
        
        
        #Ensure database is created
        create_database()

        # Background Image
        self.bgImage = self.load_image("./image/background img.png")
        if self.bgImage:
            bgLabel = tk.Label(self.root, image=self.bgImage)
            bgLabel.place(x=0, y=0)

        # UI Elements
        self.create_ui()

    def load_image(self, path):
        try:
            return ImageTk.PhotoImage(file=path)
        except Exception as e:
            print(f"Error loading image '{path}': {e}")
            return None

    def create_ui(self):
        # Heading
        heading = tk.Label(
            self.root, text="Welcome to Driver Login", font=("Aptos Black", 16, "bold"), bg="white", fg="#FFC107"
        )
        heading.place(x=590, y=100)

        # Email Entry
        self.email_entry = tk.Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray")
        self.email_entry.place(x=550, y=200)
        self.email_entry.insert(0, "Email")
        self.email_entry.bind("<FocusIn>", self.email_enter)
        self.email_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.email_entry, "Email"))
        tk.Frame(self.root, width=325, height=2, bg="#0275d8").place(x=550, y=225)

        # Password Entry
        self.password_entry = tk.Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray", show="*")
        self.password_entry.place(x=550, y=290)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", self.password_enter)
        self.password_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.password_entry, "Password"))
        tk.Frame(self.root, width=325, height=2, bg="#0275d8").place(x=550, y=315)

        # Login Button
        loginButton = tk.Button(
            self.root,
            text="Login",
            font=("Aptos Black", 14, "bold"), fg="white", bg="#0275d8", activeforeground="yellow",
            activebackground="#025aa5", cursor="hand2", bd=0, width=19, command=self.login_user
        )
        loginButton.place(x=600, y=365)

        # OR Label
        orLabel = tk.Label(
            self.root,
            text="----------------------------OR----------------------------",
            font=("Aptos Black", 12, "bold"), fg="#FFC107", bg="white"
        )
        orLabel.place(x=565, y=420)

        # Sign-Up Label
        signupLabel = tk.Label(self.root, text="Don't have an account?", font=("Aptos Black", 12), fg="#FFC107", bg="white")
        signupLabel.place(x=640, y=450)

        # Create Account Buttons
        customerButton = tk.Button(
            self.root, text="Create as a Driver",
            font=("Aptos Black", 12, "bold underline"), fg="#0275d8", activeforeground="#FFC107",
            activebackground="yellow", cursor="hand2", bd=0, width=19, command=self.register_user
        )
        customerButton.place(x=620, y=490)
        
        # Back Button
        backButton = tk.Button(
            self.root,
            text="Back",
            font=("Aptos Black", 12, "bold"), fg="white", bg="#d9534f", activeforeground="white", activebackground="#c9302c", cursor="hand2",
            bd=0, width=10, command=self.go_back,
        )
        backButton.place(x=20, y=20)


    def reset_placeholder(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")
        else:
            entry.config(fg="black")

    def email_enter(self, event):
        if self.email_entry.get() == "Email":
            self.email_entry.delete(0, "end")
        self.email_entry.config(fg="black")
        
    

    def password_enter(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, "end")
        self.password_entry.config(fg="black")


        
    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or email == "Email":
            messagebox.showerror("Error", "Please enter your email.")
            return
        if not password or password == "Password":
            messagebox.showerror("Error", "Please enter your password.")
            return
        
        # Assuming check_credentials_driver returns the driver_id along with True/False status
        driver_id = check_credentials_driver(email, password)
        
        if driver_id:
            messagebox.showinfo("Success", "Login successful!")
            # Redirect to the driver dashboard, passing the driver_id
            import driver_dashboard
            self.new_window = tk.Toplevel(self.root)
            driver_dashboard.DriverDashboardApp(self.new_window, driver_id)  # Pass driver_id here
        else:
            messagebox.showerror("Error", "Invalid email or password.")
        
    def register_user(self):
        self.root.destroy()
        import signup_driver
        signup_driver.signupDriverApp(tk.Tk())
    
    
    def go_back(self):
        """Closes the current window and reopens the main login page (main.py)."""
        self.root.destroy()
        import main  # Import the main.py file, which is your entry point
        main.main()  # Assuming main.py has a main() function to initialize the app


#--------------------------------------------------------- Main ----------------------------------------------------------------------#

if __name__ == "__main__":
    root = tk.Tk()
    app = DriverLoginApp(root)
    root.mainloop()
