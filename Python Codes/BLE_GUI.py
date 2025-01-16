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
import struct


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
# global variables for buttons
button_1_state = 0
button_2_state = 0
button_3_state = 0
current_time = 0


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
# image_label_LED_4 = tk.Label(root, image=LED_4_image)
# image_label_LED_4.grid(row=0, column=4, padx=(5, 10), pady=(10, 10), sticky='ne')  # Positioned to the right

LED_ON_images = [LED_ON_1_image, LED_ON_2_image, LED_ON_3_image]
LED_OFF_images = [LED_1_image, LED_2_image, LED_3_image]
image_label_list = [image_label_LED_1, image_label_LED_2, image_label_LED_3]

# Functions for buttons
def Connect():
    asyncio.run_coroutine_threadsafe(connect_to_device(), loop)

def Disconnect():
    asyncio.run_coroutine_threadsafe(disconnect_from_device(), loop)

# def LED_1_Toggle():
#     led_states[0] = not led_states[0]
#     image_label_LED_1.config(image=LED_ON_1_image if led_states[0] else LED_1_image)
#     update_status("LED 1 toggled to ON" if led_states[0] else "LED 1 toggled to OFF")
#     data_to_send = b"LED 1 ON"


def LED_Toggle(led_number):
    if 1 <= led_number <= 3:
        led_states[led_number - 1] = not led_states[led_number - 1]
        image_label_list[led_number - 1].config(
        image=LED_ON_images[led_number - 1] if led_states[led_number - 1] else LED_OFF_images[led_number - 1]
        )
        led_status = "ON" if led_states[led_number - 1] else "OFF"
        update_status(f"LED {led_number} toggled to {led_status}")
        data_to_send = bytearray(5)
        data_to_send[led_number] = 1 if led_states[led_number - 1] else 0
        asyncio.run(send_data_to_nucleo(data_to_send))
    else:
        update_status("Invalid LED number")

# function to update status
def update_status(message):
    status_textbox.config(state="normal")  # turn on editing
    status_textbox.insert("end", f"{message}\n")  # newline
    status_textbox.see("end")  # scroll to the end
    status_textbox.config(state="disabled")  # turn off editinG
    # Aktualizacja stanu przycisków

# function to update status
def update_BLE_DATA(message):
    BLE_data_textbox.config(state="normal")  # turn on editing
    BLE_data_textbox.insert("end", f"{message}\n")  # newline
    BLE_data_textbox.see("end")  # scroll to the end
    BLE_data_textbox.config(state="disabled")  # turn off editing
    Button_1_state.config(text=f"Button 1: {'ON' if button_1_state == 1 else 'OFF'}")
    Button_2_state.config(text=f"Button 2: {'ON' if button_2_state == 1 else 'OFF'}")
    Button_3_state.config(text=f"Button 3: {'ON' if button_3_state == 1 else 'OFF'}")

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

def decode_ble_payload(data):
    """
    Dekoduje dane BLE na podstawie struktury BLE_Payload:
    uint8_t button_state;
    uint32_t current_time;
    """
    global button_1_state, button_2_state, button_3_state, current_time
    # Rozmiar struktury BLE_Payload
    expected_length = 7  # 1 bajt (button_state) + 4 bajty (current_time)
    #print(f"data: {data}")
    # Sprawdź, czy dane mają odpowiednią długość
    if len(data) < expected_length:
        print(f"Error: Received data too short ({len(data)} bytes, expected {expected_length} bytes)\n Data: {data}")
        return None, None

    # Skróć dane do oczekiwanej długości (jeśli za długie)
    trimmed_data = data[:expected_length]

    # Struktura C: 1 bajt (button_state) + 4 bajty (current_time)
    format_string = "<B B B I"  # Little-endian: B (uint8_t), I (uint32_t)
    try:
        button_1_state, button_2_state, button_3_state, current_time = struct.unpack(format_string, trimmed_data)
        return button_1_state, button_2_state, button_3_state, current_time
    except struct.error as e:
        print(f"Error decoding BLE payload: {e}")
        return None, None


# Function to process notifications
def process_notifications():
    while not notification_queue.empty():
        sender, data = notification_queue.get()

        # Dekoduj dane BLE
        button_1_state, button_2_state, button_3_state, current_time = decode_ble_payload(data)
        # Sprawdź, czy dane zostały poprawnie zdekodowane
        # if current_time is not None:
        #     # Wyświetl dane w czytelnej formie
        #     update_BLE_DATA(
        #       #  f"Data received from {sender}: Button 1 State={button_1_state},Button 2 State={button_2_state},Button 3 State={button_3_state}, Current Time={current_time} seconds"
        #     )
        # else:
        #     update_BLE_DATA(f"Data received from {sender}: Invalid payload")
        update_BLE_DATA(f"Data: {current_time}")
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
# text status 
# Area for status

status_frame = ttk.LabelFrame(root, text="Status")
status_frame.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

status_textbox = tk.Text(status_frame, wrap="word", height=5)
status_textbox.pack(fill="both", expand=True, padx=5, pady=5)
status_textbox.config(state="disabled")

asyncio_thread = threading.Thread(target=start_asyncio_loop, daemon=True) 
asyncio_thread.start()

# Frame for buttons
button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, pady=(10, 10), padx=(10, 5), sticky='nw')

#Conntecting and Disconnecting buttons
open_button=ttk.Button(button_frame, text='Connect', command=Connect, 
                         style='BigFont.TButton', width=20)
open_button.grid(row=0, column=0, padx=5, pady=5)

disconnect_button=ttk.Button(button_frame, text='Disconnect', command=Disconnect, 
                         style='BigFont.TButton', width=20)
disconnect_button.grid(row=0, column=1, padx=5, pady=5)

Button_1_state = ttk.Label(button_frame, text="Button 1: OFF", font=('Helvetica', 12))
Button_1_state.grid(row=1, column=0, columnspan=1, pady=0)

Button_2_state = ttk.Label(button_frame, text="Button 2: OFF", font=('Helvetica', 12))
Button_2_state.grid(row=1, column=1, columnspan=1, pady=0)

Button_3_state = ttk.Label(button_frame, text="Button 3: OFF", font=('Helvetica', 12))
Button_3_state.grid(row=2, column=0, columnspan=1, pady=0)

Button_4_state = ttk.Label(button_frame, text="Button 4: OFF", font=('Helvetica', 12))
Button_4_state.grid(row=2, column=1, columnspan=1, pady=0)

#Buttons under the images 
button_LED_1 = ttk.Button(root, text="Control LED 1", command=lambda: LED_Toggle(1))#labda for passing arguments to function because normally it would be called immediately
button_LED_1.grid(row=1, column=1, pady=(5, 10), padx=5, sticky='n')

button_LED_2 = ttk.Button(root, text="Control LED 2", command=lambda: LED_Toggle(2))
button_LED_2.grid(row=1, column=2, pady=(5, 10), padx=5, sticky='n')

button_LED_3 = ttk.Button(root, text="Control LED 3", command=lambda: LED_Toggle(3))
button_LED_3.grid(row=1, column=3, pady=(5, 10), padx=5, sticky='n')

# button_LED_4 = ttk.Button(root, text="Control LED 4", command=LED_Toggle(4))
# button_LED_4.grid(row=1, column=4, pady=(5, 10), padx=5, sticky='n')

# Area for BLE Data
BLE_data_frame = ttk.LabelFrame(root, text="BLE Data")
BLE_data_frame.grid(row=3, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

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