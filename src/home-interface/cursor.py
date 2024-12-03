import pinching_at_location_example
from pinching_at_location_example import MyListener as Listener
import leap


import time


import tkinter as tk
import tkinter.ttk as ttk


# print(Listener)
new_listener = Listener()
connection = leap.Connection()
connection.add_listener(new_listener)






with connection.open(): # make sure that all gui stuff is contained within this . this makes sure that the connection stay open
   new_listener.set_tracking_frame_size(1)
  
   window = tk.Tk()
   coordinates = tk.StringVar()
   coords_label = tk.Label(window, textvariable=coordinates)
   coords_label.pack()


   window.resizable(0,0)
   window.wm_attributes("-topmost", 1)
   canvas = tk.Canvas(window, width=600, height=600, bd=0, highlightthickness=0)
   canvas.pack()


   quit = False


   def quit_func():
       global quit
       quit = True


   box_size = 10
   box = canvas.create_rectangle(0,0,box_size, box_size, fill = "black")


   quit_button = tk.Button(text = "quit", command = quit_func)
   quit_button.pack()
  
   while not quit:
       coordinates.set((new_listener.get_palm_position()[0]+300, new_listener.get_palm_position()[2]+300))


       canvas.moveto(box, new_listener.get_palm_position()[0]+300, new_listener.get_palm_position()[2]+300)


       window.update()
  
   window.destroy()
