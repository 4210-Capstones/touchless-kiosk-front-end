import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

class TouchlessKioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Touchless Kiosk")

        # Fullscreen window
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # Initialize screen size
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Load the initial background image for the home screen
        self.load_background("./assets/background-images/stock-background.png")

        # Create a frame to hold everything (background + buttons)
        self.main_frame = None
        self.create_main_screen()

    def load_background(self, image_path):
        """Load the background image from the given path."""
        self.background = Image.open(image_path)

        # Resize the image to fit the screen size
        self.background = self.background.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)

    def create_main_screen(self):
        """Create the main screen and its buttons."""
        # Create a new frame for the home screen
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Create the canvas for the background image
        self.canvas = tk.Canvas(self.main_frame, width=self.screen_width, height=self.screen_height)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)  # Fill the entire frame

        # Place the background image on the canvas
        self.bg_image = ImageTk.PhotoImage(self.background)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Create a frame for buttons to sit on top of the background
        self.button_frame = tk.Frame(self.main_frame, bg='black')  # Transparent background for buttons
        self.button_frame.place(relx=0.5, rely=0.8, anchor="center")  # Position it at the bottom center

        # Create buttons for 'Students', 'Faculty', 'UNO Partners'
        self.create_main_screen_buttons()

    def create_main_screen_buttons(self):
        """Create buttons for 'Students', 'Faculty', 'UNO Partners' on the main screen."""
        # Create the three buttons on the main screen
        self.button_students = tk.Button(self.button_frame, text="Students", width=20, height=3, bg="white", fg="black")
        self.button_students.grid(row=0, column=0, padx=20)

        self.button_faculty = tk.Button(self.button_frame, text="Faculty", width=20, height=3, bg="white", fg="black")
        self.button_faculty.grid(row=0, column=1, padx=20)

        # UNO Partners button which turns into a dropdown menu
        self.button_uno_partners = tk.Button(self.button_frame, text="UNO Partners", width=20, height=3, bg="white", fg="black", command=self.show_uno_partners_dropdown)
        self.button_uno_partners.grid(row=0, column=2, padx=20)

    def show_uno_partners_dropdown(self):
        """Hide the UNO Partners button and show the dropdown."""
        # Hide the "UNO Partners" button
        self.button_uno_partners.grid_forget()

        # List of UNO Partners (AIR Lab, GulfSCEI)
        partners = ["AIR Lab", "GulfSCEI"]

        # Create a dropdown menu (OptionMenu)
        self.selected_partner = tk.StringVar()  # Variable to hold selected value
        self.uno_partners_dropdown = tk.OptionMenu(self.button_frame, self.selected_partner, *partners)
        self.uno_partners_dropdown.config(width=20, height=2, bg="white", fg="black")
        self.uno_partners_dropdown.grid(row=0, column=2, padx=20)

        # Add a button to confirm the selection
        self.button_confirm_selection = tk.Button(self.button_frame, text="Select", width=10, height=2, bg="white", fg="black", command=self.handle_partner_selection)
        self.button_confirm_selection.grid(row=1, column=2, padx=20)

    def handle_partner_selection(self):
        """Handle the event when a partner is selected from the dropdown."""
        selected_partner = self.selected_partner.get()
        print(f"Selected UNO Partner: {selected_partner}")

        # Hide the dropdown and selection button
        self.uno_partners_dropdown.grid_forget()
        self.button_confirm_selection.grid_forget()

        # Update the background based on the selected partner
        if selected_partner == "AIR Lab":
            self.load_background("./assets/background-images/airlab-partner-background.png")
        elif selected_partner == "GulfSCEI":
            self.load_background("./assets/background-images/gulfscei-partner-background.png")

        # Recreate the background and buttons on the screen for the selected partner
        self.create_background_and_buttons(selected_partner)

    def create_background_and_buttons(self, partner):
        """Create the updated background and buttons after selecting a partner."""
        # Recreate the canvas for the background image
        self.canvas = tk.Canvas(self.main_frame, width=self.screen_width, height=self.screen_height)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)  # Fill the entire frame

        # Place the new background image on the canvas
        self.bg_image = ImageTk.PhotoImage(self.background)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Create a frame for buttons to sit on top of the new background
        self.button_frame = tk.Frame(self.main_frame, bg='black')  # Transparent background for buttons
        self.button_frame.place(relx=0.5, rely=0.8, anchor="center")  # Position it at the bottom center

        # Create new buttons based on the partner selected
        if partner == "AIR Lab" or partner == "GulfSCEI":
            self.create_partner_buttons(partner)

    def create_partner_buttons(self, partner):
        """Create buttons for 'Past Research', 'Ongoing Research', 'Demo Videos'."""
        # Create the new buttons for the selected partner
        self.button_past_research = tk.Button(self.button_frame, text="Past Research", width=20, height=3, bg="white", fg="black", command=self.past_research_action)
        self.button_past_research.grid(row=0, column=0, padx=20)

        self.button_ongoing_research = tk.Button(self.button_frame, text="Ongoing Research", width=20, height=3, bg="white", fg="black", command=self.ongoing_research_action)
        self.button_ongoing_research.grid(row=0, column=1, padx=20)

        self.button_demo_videos = tk.Button(self.button_frame, text="Demo Videos", width=20, height=3, bg="white", fg="black", command=self.demo_videos_action)
        self.button_demo_videos.grid(row=0, column=2, padx=20)

        # Add the "Main Menu" button
        self.button_main_menu = tk.Button(self.button_frame, text="Main Menu", width=20, height=3, bg="white", fg="black", command=self.return_to_main_menu)
        self.button_main_menu.grid(row=1, column=1, padx=20)

    def past_research_action(self):
        """Placeholder function for Past Research button click."""
        print("Past Research clicked")

    def ongoing_research_action(self):
        """Placeholder function for Ongoing Research button click."""
        print("Ongoing Research clicked")

    def demo_videos_action(self):
        """Placeholder function for Demo Videos button click."""
        print("Demo Videos clicked")

    def return_to_main_menu(self):
        """Return to the main menu."""
        print("Returning to Main Menu")

        # Clear the current screen and reset to the home screen
        self.main_frame.destroy()

        # Re-load the home screen background and recreate the main screen
        self.load_background("./assets/background-images/stock-background.png")  # Reset to home screen background
        self.create_main_screen()  # Create the buttons and main screen again

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = TouchlessKioskApp(root)
    root.mainloop()
