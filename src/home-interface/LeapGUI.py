import tkinter as tk
from tkinter import ttk
import requests
import camera_bindings
from camera_bindings import MyListener as Listener
import leap
import macmouse

# Initialize Leap Motion Listener and Connection
new_listener = Listener()
connection = leap.Connection()
connection.add_listener(new_listener)

# Define API URL
API_BASE_URL = "http://localhost:8000/"  


def fetch_upcoming_events():
    """
    Fetch upcoming events from the API.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/events/upcoming")
        response.raise_for_status()
        events = response.json()  # Assuming its json
        return events
    except requests.RequestException as e:
        print(f"Error fetching events: {e}")
        return None


def display_events():
    """
    Display upcoming events in the GUI.
    """
    events = fetch_upcoming_events()
    if not events:
        events_frame = tk.Label(main_frame, text="Failed to load events.", fg="red", font=("Arial", 18, "bold"))
        events_frame.pack()
        return

    # Update UI with events
    events_frame = tk.Frame(main_frame, bg="white")
    events_frame.pack(fill=tk.BOTH, expand=True)
    for event in events:
        event_label = tk.Label(events_frame, text=f"{event['name']} - {event['date']}", font=("Arial", 14), bg="white")
        event_label.pack(pady=5)


# GUI Initialization
with connection.open():
    new_listener.set_tracking_frame_size(1)
    root = tk.Tk()
    root.title("Welcome")
    root.geometry("700x500")

    # Configuring main frame
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True)

    welcomeLabel = tk.Label(
        main_frame,
        text="WELCOME, SELECT ONE OF THE OPTIONS.",
        font=("Arial", 25, "bold"),
        fg="blue",
        bg="white"
    )
    welcomeLabel.pack(pady=20)

    buttons_frame = tk.Frame(main_frame, bd=5, bg="white")
    buttons_frame.pack(fill=tk.BOTH, padx=20, pady=20, expand=True)

    buttons_frame.columnconfigure(0, weight=1)
    buttons_frame.columnconfigure(1, weight=1)
    buttons_frame.rowconfigure(0, weight=1)
    buttons_frame.rowconfigure(1, weight=1)

    # Creating style for buttons
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Blue.TButton",
        font=("Arial", 18, "bold"),
        background="blue",
        foreground="white",
        padding=10,
        relief="flat"
    )
    style.map(
        "Blue.TButton",
        background=[("active", "lightblue"), ("!active", "blue")],
        foreground=[("active", "blue"), ("!active", "white")]
    )

    # Create buttons with the custom style
    student_button = ttk.Button(
        buttons_frame,
        command=lambda: print("Student Login"),  # Replace with actual logic
        text="STUDENT LOGIN",
        style="Blue.TButton"
    )
    faculty_button = ttk.Button(
        buttons_frame,
        command=lambda: print("Faculty Login"),  # Replace with actual logic
        text="FACULTY LOGIN",
        style="Blue.TButton"
    )
    map_button = ttk.Button(
        buttons_frame,
        command=lambda: print("3rd Floor Map"),  # Replace with actual logic
        text="3RD FLOOR MAP",
        style="Blue.TButton"
    )
    event_button = ttk.Button(
        buttons_frame,
        command=display_events,
        text="UPCOMING EVENTS",
        style="Blue.TButton"
    )

    # Layout with spacing
    student_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.S + tk.N)
    faculty_button.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W + tk.E + tk.S + tk.N)
    map_button.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.S + tk.N)
    event_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W + tk.E + tk.S + tk.N)

    # Leap Motion Integration
    pinching = False
    while True:
        macmouse.move(
            (new_listener.get_palm_position()[0]) * (1920 / 500) + (1920 / 2),
            (new_listener.get_palm_position()[2]) * (1080 / 500) + (1080 / 2)
        )
        if new_listener.is_pinching():
            pinching = True
            print("Pinching")
        else:
            if pinching:
                pinching = False
                macmouse.click()

        root.update_idletasks()
        root.update()
