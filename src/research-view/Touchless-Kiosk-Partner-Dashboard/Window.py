import tkinter as tk 
from tkinter import ttk

import camera_bindings
from camera_bindings import MyListener as Listener
import leap
import macmouse # import mouse for linux and windows

new_listener = Listener()
connection = leap.Connection()
connection.add_listener(new_listener)

with connection.open(): # gui should be contained in this block

    # this makes movements smoother
    new_listener.set_tracking_frame_size(1)
 
    # Initialize main window
    root = tk.Tk()
    root.title("Welcome")
    root.geometry("700x500")
    
    # Configuring main frame 
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True)
    welcomeLabel = tk.Label(main_frame, text="WELCOME, SELECT ONE OF THE OPTIONS.", font=("Arial", 25, "bold"), fg="blue", bg="white")
    welcomeLabel.pack(pady=20)
    buttons_frame = tk.Frame(
        main_frame, bd=5, bg="white"
    )
    buttons_frame.pack(fill=tk.BOTH, padx=20, pady=20, expand=True)
    buttons_frame.columnconfigure(0, weight=1)
    buttons_frame.columnconfigure(1, weight=1)
    buttons_frame.rowconfigure(0, weight=1)
    buttons_frame.rowconfigure(1, weight=1)

    # Creating style for buttons 
    style = ttk.Style()
    style.theme_use("clam")  # Use a simple, cross-platform theme to avoid OS-specific styles
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
    student_button = ttk.Button(buttons_frame, command= student_window, text="STUDENT LOGIN", style="Blue.TButton")
    faculty_button = ttk.Button(buttons_frame, text="FACULTY LOGIN", style="Blue.TButton")
    map_button = ttk.Button(buttons_frame, text="3RD FLOOR MAP", style="Blue.TButton")
    event_button = ttk.Button(buttons_frame, text="UPCOMING EVENTS", style="Blue.TButton")

    # Layout with spacing
    student_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.S + tk.N)
    faculty_button.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W + tk.E + tk.S + tk.N)
    map_button.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.S + tk.N)
    event_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W + tk.E + tk.S + tk.N)
    
    # function to display the student window
    def student_window():
       main_frame.pack_forget()
       student_frame = tk.Frame(root, bg="white")
       student_frame.pack(fill=tk.BOTH, expand=True) 
       student_label = tk.Label(student_frame, text="**Displaying student frame**", font=("Arial", 28, "bold"))
       student_label.pack(pady=20)

    pinching = False

    while True:
        # print(new_listener.get_palm_position())
        
        # detect movement of the palm and move the cursor 
        macmouse.move((new_listener.get_palm_position()[0])*(1920/500)+(1920/2), (new_listener.get_palm_position()[2])*(1920/500)+(1080/2))
        
        if new_listener.is_pinching():
            pinching = True
            print("Pinching")
        else:
            if pinching:
                pinching = False
                macmouse.click()    
        
        # update window
        root.update_idletasks()
        root.update()