import asyncio
import logging
from bleak import BleakClient
import struct
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Use Pillow for image resizin

root = tk.Tk()
root.title('BLE GUI')
root.resizable(True,True)
root.geometry('1200x900')
root.columnconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.update()

style = ttk.Style()
style.configure('SmallFont.TButton', font=('Helvetica', 18))

original_image = Image.open("LED.png")
LED_1_orginal_image= original_image.resize((150, 150))  # Resize to 150x150 pixels
LED_2_orginal_image= original_image.resize((150, 150))  # Resize to 150x150 pixels
LED_3_orginal_image= original_image.resize((150, 150))  # Resize to 150x150 pixels
LED_4_orginal_image= original_image.resize((150, 150))  # Resize to 150x150 pixels

LED_1_image = ImageTk.PhotoImage(LED_1_orginal_image)
LED_2_image = ImageTk.PhotoImage(LED_2_orginal_image)
LED_3_image = ImageTk.PhotoImage(LED_3_orginal_image)
LED_4_image = ImageTk.PhotoImage(LED_4_orginal_image)


image_label_LED_1 = tk.Label(root, image=LED_1_image)
image_label_LED_1.grid(row=0, column=1, padx=(5, 10), pady=(10, 10), sticky='e')  # Positioned to the right
image_label_LED_2 = tk.Label(root, image=LED_2_image)
image_label_LED_2.grid(row=0, column=2, padx=(5, 10), pady=(10, 10), sticky='e')  # Positioned to the right
image_label_LED_3 = tk.Label(root, image=LED_3_image)
image_label_LED_3.grid(row=0, column=3, padx=(5, 10), pady=(10, 10), sticky='e')  # Positioned to the right
image_label_LED_4 = tk.Label(root, image=LED_4_image)
image_label_LED_4.grid(row=0, column=4, padx=(5, 10), pady=(10, 10), sticky='e')  # Positioned to the right

NUCLEO_ADDRESS = "00:80:E1:22:E5:13"
NOTIFY_CHARACTERISTIC_UUID = "00001000-8e22-4541-9d4c-21edae82ed19"  # UUID charakterystyki do notyfikacji

def Connect():
       print(f"Łączenie z urządzeniem {NUCLEO_ADDRESS}...")

def Disconnect():
       print(f"Łączenie z urządzeniem {NUCLEO_ADDRESS}...")


button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, pady=(10, 10), padx=(10, 5), sticky='nw')


open_button=ttk.Button(button_frame, text='Connect', command=Connect, 
                         style='BigFont.TButton', width=20)
open_button.grid(row=0, column=0, padx=5, pady=5)

open_button=ttk.Button(button_frame, text='Connect', command=Disconnect, 
                         style='BigFont.TButton', width=20)
open_button.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()