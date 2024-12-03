import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import leap
import macmouse

class TouchlessKioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Touchless Kiosk")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # Initialize screen size
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Load the initial background image for the home screen
        self.load_background("./assets/background-images/stock-background.png")

        # Create main screen layout
        self.create_main_screen()

        # Leap Motion Setup
        self.leap_listener = leap.Listener()
        self.leap_connection = leap.Connection()
        self.leap_connection.add_listener(self.leap_listener)
        self.is_pinching = False

        # Start custom update loop
        self.run_loop()

    def load_background(self, image_path):
        self.background = Image.open(image_path)
        self.background = self.background.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)

    def create_main_screen(self):
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
        self.button_students = tk.Button(self.button_frame, text="Students", width=20, height=3, bg="white", fg="black")
        self.button_students.grid(row=0, column=0, padx=20)

        self.button_faculty = tk.Button(self.button_frame, text="Faculty", width=20, height=3, bg="white", fg="black")
        self.button_faculty.grid(row=0, column=1, padx=20)

        self.button_uno_partners = tk.Button(self.button_frame, text="UNO Partners", width=20, height=3, bg="white", fg="black", command=self.show_uno_partners_dropdown)
        self.button_uno_partners.grid(row=0, column=2, padx=20)

    def run_loop(self):
        with self.leap_connection.open():
            while True:
                # Leap Motion tracking logic
                palm_position = self.leap_listener.get_palm_position()
                cursor_x = palm_position[0] * (self.screen_width / 500) + (self.screen_width / 2)
                cursor_y = palm_position[2] * (self.screen_height / 500) + (self.screen_height / 2)
                macmouse.move(cursor_x, cursor_y)

                if self.leap_listener.is_pinching():
                    if not self.is_pinching:
                        self.is_pinching = True
                        macmouse.click()
                else:
                    self.is_pinching = False

                # Update GUI frame by frame
                self.root.update_idletasks()
                self.root.update()

    def show_uno_partners_dropdown(self):
        self.button_uno_partners.grid_forget()
        partners = ["AIR Lab", "GulfSCEI"]
        self.selected_partner = tk.StringVar()
        self.uno_partners_dropdown = tk.OptionMenu(self.button_frame, self.selected_partner, *partners)
        self.uno_partners_dropdown.config(width=20, height=2, bg="white", fg="black")
        self.uno_partners_dropdown.grid(row=0, column=2, padx=20)
        self.button_confirm_selection = tk.Button(self.button_frame, text="Select", width=10, height=2, bg="white", fg="black", command=self.handle_partner_selection)
        self.button_confirm_selection.grid(row=1, column=2, padx=20)

    def handle_partner_selection(self):
        selected_partner = self.selected_partner.get()
        print(f"Selected UNO Partner: {selected_partner}")
        self.uno_partners_dropdown.grid_forget()
        self.button_confirm_selection.grid_forget()
        self.load_background(f"./assets/background-images/{selected_partner.lower()}-partner-background.png")
        self.create_background_and_buttons(selected_partner)

    def create_background_and_buttons(self, partner):
        self.canvas = tk.Canvas(self.main_frame, width=self.screen_width, height=self.screen_height)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_image = ImageTk.PhotoImage(self.background)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.button_frame = tk.Frame(self.main_frame, bg='black')
        self.button_frame.place(relx=0.5, rely=0.8, anchor="center")
        self.create_partner_buttons(partner)

    def create_partner_buttons(self, partner):
        self.button_past_research = tk.Button(self.button_frame, text="Past Research", width=20, height=3, bg="white", fg="black", command=self.past_research_action)
        self.button_past_research.grid(row=0, column=0, padx=20)
        self.button_ongoing_research = tk.Button(self.button_frame, text="Ongoing Research", width=20, height=3, bg="white", fg="black", command=self.ongoing_research_action)
        self.button_ongoing_research.grid(row=0, column=1, padx=20)
        self.button_demo_videos = tk.Button(self.button_frame, text="Demo Videos", width=20, height=3, bg="white", fg="black", command=self.demo_videos_action)
        self.button_demo_videos.grid(row=0, column=2, padx=20)
        self.button_main_menu = tk.Button(self.button_frame, text="Main Menu", width=20, height=3, bg="white", fg="black", command=self.return_to_main_menu)
        self.button_main_menu.grid(row=1, column=1, padx=20)

    def past_research_action(self):
        print("Past Research clicked")

    def ongoing_research_action(self):
        print("Ongoing Research clicked")

    def demo_videos_action(self):
        print("Demo Videos clicked")

    def return_to_main_menu(self):
        print("Returning to Main Menu")
        self.main_frame.destroy()
        self.load_background("./assets/background-images/stock-background.png")
        self.create_main_screen()

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = TouchlessKioskApp(root)