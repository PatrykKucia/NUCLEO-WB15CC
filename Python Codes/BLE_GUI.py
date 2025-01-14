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

led_states = [False, False, False, False]


LED_1_orginal_image = Image.open("LED.png")
LED_1_orginal_image= LED_1_orginal_image.resize((120, 200))  # Resize to 150x150 pixels
LED_2_orginal_image= LED_1_orginal_image.resize((120, 200))  # Resize to 150x150 pixels
LED_3_orginal_image= LED_1_orginal_image.resize((120, 200))  # Resize to 150x150 pixels
LED_4_orginal_image= LED_1_orginal_image.resize((120, 200))  # Resize to 150x150 pixels

LED_1_image = ImageTk.PhotoImage(LED_1_orginal_image)
LED_2_image = ImageTk.PhotoImage(LED_2_orginal_image)
LED_3_image = ImageTk.PhotoImage(LED_3_orginal_image)
LED_4_image = ImageTk.PhotoImage(LED_4_orginal_image)


LED_ON_1_orginal_image = Image.open("LED_ON.png")
LED_ON_1_orginal_image= LED_ON_1_orginal_image.resize((120, 200))  # Resize to 150x150 pixels
LED_ON_2_orginal_image= LED_ON_1_orginal_image.resize((120, 200))  # Resize to 150x150 pixels
LED_ON_3_orginal_image= LED_ON_1_orginal_image.resize((120, 200))  # Resize to 150x150 pixels
LED_ON_4_orginal_image= LED_ON_1_orginal_image.resize((120, 200))  # Resize to 150x150 pixels

LED_ON_1_image = ImageTk.PhotoImage(LED_ON_1_orginal_image)
LED_ON_2_image = ImageTk.PhotoImage(LED_ON_2_orginal_image)
LED_ON_3_image = ImageTk.PhotoImage(LED_ON_3_orginal_image)
LED_ON_4_image = ImageTk.PhotoImage(LED_ON_4_orginal_image)
 



image_label_LED_1 = tk.Label(root, image=LED_1_image)
image_label_LED_1.grid(row=0, column=1, padx=(5, 10), pady=(10, 10), sticky='ne')  # Positioned to the right
image_label_LED_2 = tk.Label(root, image=LED_2_image)
image_label_LED_2.grid(row=0, column=2, padx=(5, 10), pady=(10, 10), sticky='ne')  # Positioned to the right
image_label_LED_3 = tk.Label(root, image=LED_3_image)
image_label_LED_3.grid(row=0, column=3, padx=(5, 10), pady=(10, 10), sticky='ne')  # Positioned to the right
image_label_LED_4 = tk.Label(root, image=LED_4_image)
image_label_LED_4.grid(row=0, column=4, padx=(5, 10), pady=(10, 10), sticky='ne')  # Positioned to the right




NUCLEO_ADDRESS = "00:80:E1:22:E5:13"
NOTIFY_CHARACTERISTIC_UUID = "00001000-8e22-4541-9d4c-21edae82ed19"  # UUID charakterystyki do notyfikacji
uuid_list = [
    "00001000-8e22-4541-9d4c-21edae82ed19",  # przykładowy UUID
    "00000000-8e22-4541-9d4c-21edae82ed19",  # przykładowy UUID
]

# Functions for buttons
def Connect():
       update_status(f"connecting with device {NUCLEO_ADDRESS}...")

def Disconnect():
       update_status(f"disconnecting with device {NUCLEO_ADDRESS}...")

def LED_1_Toggle():
    led_states[0] = not led_states[0]
    image_label_LED_1.config(image=LED_ON_1_image if led_states[0] else LED_1_image)
    update_status("LED 1 toggled to ON" if led_states[0] else "LED 1 toggled to OFF")

def LED_2_Toggle():
    led_states[1] = not led_states[1]
    image_label_LED_2.config(image=LED_ON_2_image if led_states[1] else LED_2_image)
    update_status("LED 2 toggled to ON" if led_states[1] else "LED 2 toggled to OFF")

def LED_3_Toggle():
    led_states[2] = not led_states[2]
    image_label_LED_3.config(image=LED_ON_3_image if led_states[2] else LED_3_image)
    update_status("LED 3 toggled to ON" if led_states[2] else "LED 3 toggled to OFF")

def LED_4_Toggle():
    led_states[3] = not led_states[3]
    image_label_LED_4.config(image=LED_ON_4_image if led_states[3] else LED_4_image)
    update_status("LED 4 toggled to ON" if led_states[3] else "LED 4 toggled to OFF")

def update_status(message):
    status_textbox.config(state="normal")  # Włączenie edycji
    status_textbox.insert("end", f"{message}\n")  # Dodanie nowej linii
    status_textbox.see("end")  # Automatyczne przewijanie do końca
    status_textbox.config(state="disabled")  # Wyłączenie edycji


def update_BLE_address():
    global NUCLEO_ADDRESS
    new_address = address_entry.get()  #take new address
    if new_address:
        NUCLEO_ADDRESS = new_address
        update_status(f"Address changed to {NUCLEO_ADDRESS}")
    else:
        update_status("Put valid address")

def update_notify_uuid():
    global NOTIFY_CHARACTERISTIC_UUID
    selected_uuid = uuid_combobox.get()  # Pobranie wybranego UUID z comboboxa
    if selected_uuid:
        NOTIFY_CHARACTERISTIC_UUID = selected_uuid
        update_status(f"NOTIFY_CHARACTERISTIC_UUID zmieniony na {NOTIFY_CHARACTERISTIC_UUID}")
    else:
        update_status("Wybierz prawidłowy UUID!")

button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, pady=(10, 10), padx=(10, 5), sticky='nw')



#Conntecting and Disconnecting buttons
open_button=ttk.Button(button_frame, text='Connect', command=Connect, 
                         style='BigFont.TButton', width=20)
open_button.grid(row=0, column=0, padx=5, pady=5)

open_button=ttk.Button(button_frame, text='Disconnect', command=Disconnect, 
                         style='BigFont.TButton', width=20)
open_button.grid(row=0, column=1, padx=5, pady=5)

#Buttons under the images 
button_LED_1 = ttk.Button(root, text="Control LED 1", command=LED_1_Toggle)
button_LED_1.grid(row=1, column=1, pady=(5, 10), padx=5, sticky='n')

button_LED_2 = ttk.Button(root, text="Control LED 2", command=LED_2_Toggle)
button_LED_2.grid(row=1, column=2, pady=(5, 10), padx=5, sticky='n')

button_LED_3 = ttk.Button(root, text="Control LED 3", command=LED_3_Toggle)
button_LED_3.grid(row=1, column=3, pady=(5, 10), padx=5, sticky='n')

button_LED_4 = ttk.Button(root, text="Control LED 4", command=LED_4_Toggle)
button_LED_4.grid(row=1, column=4, pady=(5, 10), padx=5, sticky='n')



# Pole na status
status_frame = ttk.LabelFrame(root, text="Status")
status_frame.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)

# Tekst statusu (tk.Text)
status_textbox = tk.Text(status_frame, wrap="word", height=5)
status_textbox.pack(fill="both", expand=True, padx=5, pady=5)
status_textbox.config(state="disabled")

# Pole tekstowe do wpisania adresu
address_frame = ttk.LabelFrame(root, text="BLE address adnd UUID") 
address_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

address_label = ttk.Label(address_frame, text="BLE Address:")
address_label.grid(row=0, column=0, padx=5, pady=5)

address_entry = ttk.Entry(address_frame, font=('Helvetica', 16), width=20)
address_entry.grid(row=0, column=1, padx=5, pady=5)

# Address button
update_address_button = ttk.Button(address_frame, text="Zmień adres", command=update_BLE_address, width=20)
update_address_button.grid(row=0, column=2, padx=5, pady=5)

# Combobox with UUID
uuid_label = ttk.Label(address_frame, text="Wybierz UUID:")
uuid_label.grid(row=1, column=0, padx=5, pady=5)

uuid_combobox = ttk.Combobox(address_frame, values=uuid_list, state="readonly", width=37)
uuid_combobox.grid(row=1, column=1, padx=5, pady=5)
uuid_combobox.set(uuid_list[0])  # Ustaw domyślnie pierwszy UUID z listy

# Przycisk do zmiany UUID
update_uuid_button = ttk.Button(address_frame, text="Zmień UUID", command=update_notify_uuid, width=20)
update_uuid_button.grid(row=1, column=2, padx=5, pady=5)
update_status("Waiting for connection...")

root.mainloop()