import qrcode
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# The url you want to encode
url = "http://192.168.1.102:5001"

# Create the QR code object
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add the URL data to the QR code
qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR code
qr_img = qr.make_image(fill='black', back_color='white')

# Setup tkinter window
root = tk.Tk()
root.title("QR Code Display for Admins")

# Convert the QR code image to a format the can be used in Tkinter
qr_image_tk = ImageTk.PhotoImage(qr_img)

# Create a label to display the QR code and center it in the window
label = tk.Label(root, image=qr_image_tk)
label.pack(expand=True)

root.mainloop()
