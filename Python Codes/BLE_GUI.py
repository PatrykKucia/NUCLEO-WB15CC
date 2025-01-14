import asyncio
import logging
import threading
from bleak import BleakClient
import struct
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Use Pillow for image resizin
import queue


root = tk.Tk()
root.title('BLE GUI')
root.resizable(True,True)
root.geometry('1200x900')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)

root.rowconfigure(0, weight=1)  # Row for LED images and buttons
root.rowconfigure(1, weight=1)  # Row for LED control buttons
root.rowconfigure(2, weight=2)  # Row for Status frame
root.rowconfigure(3, weight=2)  # Row for BLE Data frame
root.rowconfigure(4, weight=1)  # Row for BLE address/UUID frame
root.update()

style = ttk.Style()
style.configure('SmallFont.TButton', font=('Helvetica', 18))

# connection status
is_connected = False
# LED states
led_states = [False, False, False, False]
#que for notifications
notification_queue = queue.Queue()
# global client 
client = None  

#adress and UUID
NUCLEO_ADDRESS = "00:80:E1:22:E5:13"
NOTIFY_CHARACTERISTIC_UUID = "00001000-8e22-4541-9d4c-21edae82ed19"  # UUID of characteristic to notify
uuid_list = [
    "00001000-8e22-4541-9d4c-21edae82ed19",  # UUID of characteristic to notify
    "00000000-8e22-4541-9d4c-21edae82ed19",  # UUID of characteristic to write char
]

#images
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

# Functions for buttons
def Connect():
    asyncio.run_coroutine_threadsafe(connect_to_device(), loop)

def Disconnect():
    asyncio.run_coroutine_threadsafe(disconnect_from_device(), loop)

def LED_1_Toggle():
    led_states[0] = not led_states[0]
    image_label_LED_1.config(image=LED_ON_1_image if led_states[0] else LED_1_image)
    update_status("LED 1 toggled to ON" if led_states[0] else "LED 1 toggled to OFF")
    data_to_send = b"LED 1 ON"
    asyncio.run(send_data_to_nucleo(data_to_send))

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

# function to update status
def update_status(message):
    status_textbox.config(state="normal")  # turn on editing
    status_textbox.insert("end", f"{message}\n")  # newline
    status_textbox.see("end")  # scroll to the end
    status_textbox.config(state="disabled")  # turn off editing

# function to update status
def update_BLE_DATA(message):
    BLE_data_textbox.config(state="normal")  # turn on editing
    BLE_data_textbox.insert("end", f"{message}\n")  # newline
    BLE_data_textbox.see("end")  # scroll to the end
    BLE_data_textbox.config(state="disabled")  # turn off editing

# Function to update BLE address
def update_BLE_address():
    global NUCLEO_ADDRESS
    new_address = address_entry.get()  #take new address
    if new_address:
        NUCLEO_ADDRESS = new_address
        update_status(f"Address changed to {NUCLEO_ADDRESS}")
    else:
        update_status("Put valid address")

# Function to update UUID
def update_notify_uuid():
    global NOTIFY_CHARACTERISTIC_UUID
    selected_uuid = uuid_combobox.get()  # Pobranie wybranego UUID z comboboxa
    if selected_uuid:
        NOTIFY_CHARACTERISTIC_UUID = selected_uuid
        update_status(f"UUID changed to {NOTIFY_CHARACTERISTIC_UUID}")
    else:
        update_status("Put valid UUID!")

# Function to send data to Nucleo
async def send_data_to_nucleo(data_to_send):
    try:
            if client.is_connected:
                print(f"Sending Data: {data_to_send}")
                await client.write_gatt_char(NOTIFY_CHARACTERISTIC_UUID, data_to_send)
                print("Data has been send!")
    except Exception as e:
        print(f"Error in data sending: {e}")

# Function to connect to device and turn on the subscription
async def connect_to_device():
    global is_connected, client
    try:
        client = BleakClient(NUCLEO_ADDRESS)
        await client.connect()
        if client.is_connected:
            is_connected = True
            update_status("Connected to device.")
            if NOTIFY_CHARACTERISTIC_UUID == uuid_list[1]:
                update_status("Controling LEDs")
            elif NOTIFY_CHARACTERISTIC_UUID == uuid_list[0]:
                await safe_subscribe(client)  # Bezpieczne wznawianie subskrypcji
        else:
            update_status("Connection failed.")
    except Exception as e:
        update_status(f"Connection error: {e}")

# Function to safely subscribe to notifications
async def safe_subscribe(client):
    try:
        await client.start_notify(NOTIFY_CHARACTERISTIC_UUID, notification_handler)
        update_status("Subscribed to notifications.")
    except Exception as e:
        update_status(f"Subscription error: {e}")
        await asyncio.sleep(1)  # Czekaj i spróbuj ponownie
        await safe_subscribe(client)

# Function to disconnect from device
async def disconnect_from_device():
    global is_connected, client
    if client and client.is_connected:
        try:
            await client.stop_notify(NOTIFY_CHARACTERISTIC_UUID)
            await client.disconnect()
            is_connected = False
            update_status("Disconnected from STM32 NUCLEO.")
        except Exception as e:
            update_status(f"Error during disconnect: {e}")
    else:
        update_status("Not connected to any device.")

# Function to put data to queue
def notification_handler(sender, data):
    notification_queue.put((sender, data))

# Function to process notifications
def process_notifications():
    while not notification_queue.empty():
        sender, data = notification_queue.get()
        update_BLE_DATA(f"Data received from {sender}: {data}")
    root.after(100, process_notifications) # Call again after 100 ms

# Function to start asyncio loop
def start_asyncio_loop():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Start asyncio in a background thread
loop = asyncio.new_event_loop()

asyncio.set_event_loop(loop)# Uruchom asyncio w tle
asyncio_thread = threading.Thread(target=start_asyncio_loop, daemon=True)
asyncio_thread.start()
root.after(100, process_notifications) # Start processing notifications

# def monitor_asyncio():
#     if not loop.is_running():
#         update_status("Asyncio loop is not running!")
#     else:
#         update_status("Asyncio loop is running fine.")
#     root.after(5000, monitor_asyncio)  # Check every 5 seconds
#root.after(5000, monitor_asyncio)

asyncio_thread = threading.Thread(target=start_asyncio_loop, daemon=True) 
asyncio_thread.start()

# Frame for buttons
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

# Area for status
status_frame = ttk.LabelFrame(root, text="Status")
status_frame.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

# Area for BLE Data
BLE_data_frame = ttk.LabelFrame(root, text="BLE Data")
BLE_data_frame.grid(row=3, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

# text status 
status_textbox = tk.Text(status_frame, wrap="word", height=5)
status_textbox.pack(fill="both", expand=True, padx=5, pady=5)
status_textbox.config(state="disabled")

# text ble data
BLE_data_textbox = tk.Text(BLE_data_frame, wrap="word", height=5)
BLE_data_textbox.pack(fill="both", expand=True, padx=5, pady=5)
BLE_data_textbox.config(state="disabled")

# Pole tekstowe do wpisania adresu
address_frame = ttk.LabelFrame(root, text="BLE address adnd UUID") 
address_frame.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

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
uuid_combobox.set(uuid_list[0])  # Set the first UUID

# Przycisk do zmiany UUID
update_uuid_button = ttk.Button(address_frame, text="Change UUID", command=update_notify_uuid, width=20)
update_uuid_button.grid(row=1, column=2, padx=5, pady=5)

update_status("Waiting for connection...")

root.mainloop()