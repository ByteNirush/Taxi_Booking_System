import tkinter as tk 
from PIL import Image, ImageTk
from login_customer import*
from login_driver import*
from login_admin import*

#--------------------------------------------------------- Main Application Class ----------------------------------------------------------#
class mainApp:
    def __init__(self, root):
        self.root = root                                                    # Initialize the root window
        self.root.geometry("990x660+50+50")                                 # Set window size and position
        self.root.resizable(0, 0)                                           # Prevent window resizing
        self.root.title("Taxi Booking System")                              #title of page
        self.root.configure(bg="#f8f9fa")                                   #background color
#--------------------------------------------------------- Image Method ---------------------------------------------------------------------#
        self.bgImage = self.load_image("./image/background img.png")
        if self.bgImage:    
            bgLabel = tk.Label(self.root, image=self.bgImage)               # Create a label to display the image
            bgLabel.place(x=0, y=0)                                         # Place the image label in the window
    def load_image(self, path):
        try:
            return ImageTk.PhotoImage(file=path)                            # Tries to load an image from the provided path                 
        except Exception as e:
            print(f"Error loading image '{path}': {e}")                     # If an error occurs, it
            return None                                                     # Returns None if the image cannot be loaded
#======================================================= UI Creation Method ================================================================#
    def create_ui(self):
        # Heading
        heading = tk.Label(
            self.root, text="Welcome to Taxi Booking System", font=("Aptos Black", 16, "bold"), bg="white", fg="#FFC107"
        )
        heading.place(x=550, y=130)
#-------------------------------------------------------- Button Methods -------------------------------------------------------------------#
#====================================================== Customer Button======================================================================#
        customer_button = tk.Button(self.root, text="Customer", width=25, font=("Aptos Black", 14), bd=0, bg="#FFC107", 
                                    command=self.customer_action)
        customer_button.place(x=575, y=240)

#===================================================== Driver Button ========================================================================#
        driver_button = tk.Button(self.root, text="Driver", width=25, font=("Aptos Black", 14), bd=0, bg="#FFC107", 
                                command=self.driver_action)
        driver_button.place(x=575, y=340)

#======================================================= Admin Button =======================================================================#
        admin_button = tk.Button(self.root, text="Admin", width=25, font=("Aptos Black", 14), bd=0, bg="#FFC107", 
                                command=self.admin_action)
        admin_button.place(x=575, y=440)

#====================================================== Action Methods =====================================================================#
    def customer_action(self):
        CustomerLoginApp(self.root)

    def driver_action(self):
        DriverLoginApp(self.root)

    def admin_action(self):        
        AdminLoginApp(self.root)      

#========================================================= Main Execution ===================================================================#
def main():
    root = tk.Tk()
    app = mainApp(root)
    app.create_ui()
    root.mainloop()

if __name__ == "__main__":
    main()