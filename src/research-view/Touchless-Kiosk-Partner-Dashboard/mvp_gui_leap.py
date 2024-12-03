import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import macmouse
import leap
import camera_bindings
from camera_bindings import MyListener as Listener

class TouchlessKioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Touchless Kiosk")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # Screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Load the initial background image for the home screen
        self.load_background("./assets/background-images/stock-background.png")

        # Create the main screen with buttons
        self.main_frame = None
        self.create_main_screen()

        # Initialize Leap Motion Listener
        self.init_leap_motion()

    def init_leap_motion(self):
        """Initialize Leap Motion listener and connection."""
        self.new_listener = Listener()
        self.connection = leap.Connection()
        self.connection.add_listener(self.new_listener)

        # Start Leap Motion loop
        self.update_leap_motion()

    def update_leap_motion(self):
        """Update the Leap Motion tracking for cursor control."""
        if self.connection.is_connected:
            macmouse.move(
                (self.new_listener.get_palm_position()[0]) * (self.screen_width / 500) + (self.screen_width / 2),
                (self.new_listener.get_palm_position()[2]) * (self.screen_height / 500) + (self.screen_height / 2)
            )
            if self.new_listener.is_pinching():
                macmouse.click()
        
        # Schedule the next Leap update
        self.root.after(10, self.update_leap_motion)

    def load_background(self, image_path):
        """Load the background image from the given path."""
        self.background = Image.open(image_path)
        self.background = self.background.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)

    def create_main_screen(self):
        """Create the main screen and its buttons."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=self.screen_width, height=self.screen_height)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_image = ImageTk.PhotoImage(self.background)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.button_frame = tk.Frame(self.main_frame, bg='black')
        self.button_frame.place(relx=0.5, rely=0.8, anchor="center")

        self.create_main_screen_buttons()

    def create_main_screen_buttons(self):
        """Create buttons on the main screen."""
        self.button_students = tk.Button(self.button_frame, text="Students", width=20, height=3, bg="white", fg="black")
        self.button_students.grid(row=0, column=0, padx=20)

        self.button_faculty = tk.Button(self.button_frame, text="Faculty", width=20, height=3, bg="white", fg="black")
        self.button_faculty.grid(row=0, column=1, padx=20)

        self.button_uno_partners = tk.Button(self.button_frame, text="UNO Partners", width=20, height=3, bg="white", fg="black", command=self.show_uno_partners_dropdown)
        self.button_uno_partners.grid(row=0, column=2, padx=20)

    def show_uno_partners_dropdown(self):
        """Show dropdown for UNO Partners."""
        self.button_uno_partners.grid_forget()
        partners = ["AIR Lab", "GulfSCEI"]
        self.selected_partner = tk.StringVar()
        self.uno_partners_dropdown = tk.OptionMenu(self.button_frame, self.selected_partner, *partners)
        self.uno_partners_dropdown.config(width=20, height=2, bg="white", fg="black")
        self.uno_partners_dropdown.grid(row=0, column=2, padx=20)

        self.button_confirm_selection = tk.Button(self.button_frame, text="Select", width=10, height=2, bg="white", fg="black", command=self.handle_partner_selection)
        self.button_confirm_selection.grid(row=1, column=2, padx=20)

    def handle_partner_selection(self):
        """Handle partner selection."""
        selected_partner = self.selected_partner.get()
        print(f"Selected UNO Partner: {selected_partner}")
        self.uno_partners_dropdown.grid_forget()
        self.button_confirm_selection.grid_forget()
        if selected_partner == "AIR Lab":
            self.load_background("./assets/background-images/airlab-partner-background.png")
        elif selected_partner == "GulfSCEI":
            self.load_background("./assets/background-images/gulfscei-partner-background.png")
        self.create_background_and_buttons(selected_partner)

    # Add remaining button logic here...

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = TouchlessKioskApp(root)
    root.mainloop()
