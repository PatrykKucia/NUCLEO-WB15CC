import asyncio
import logging
import keyboard  # Biblioteka do obsługi klawiatury
from bleak import BleakClient
import struct

# Adres urządzenia STM32 NUCLEO (zmień na właściwy)
NUCLEO_ADDRESS = "00:80:E1:22:E5:13"

# UUID charakterystyki do notyfikacji (zmień na właściwy)
NOTIFY_CHARACTERISTIC_UUID = "00001000-8e22-4541-9d4c-21edae82ed19"  # UUID charakterystyki do notyfikacji

# Callback do obsługi notyfikacji
def notification_handler(sender, data):
    data = int.from_bytes(data, byteorder='little')
   
    print(data)   

async def connect_and_communicate():
    print(f"Łączenie z urządzeniem {NUCLEO_ADDRESS}...")
    async with BleakClient(NUCLEO_ADDRESS) as client:
        if client.is_connected:
            print("Połączono z urządzeniem STM32 NUCLEO!")

            # Subskrypcja notyfikacji
            try:
                print(f"Subskrypcja notyfikacji na charakterystyce {NOTIFY_CHARACTERISTIC_UUID}...")
                await client.start_notify(NOTIFY_CHARACTERISTIC_UUID, notification_handler)
                print("Subskrypcja aktywna.")

                # Czekanie na naciśnięcie klawisza do zakończenia subskrypcji
                print("Naciśnij 'q' aby zakończyć subskrypcję.")
                while True:
                    if keyboard.is_pressed('q'):  # Jeśli naciśnięto 'q'
                        print("Zakończenie subskrypcji...")
                        await client.stop_notify(NOTIFY_CHARACTERISTIC_UUID)
                        print("Subskrypcja została zakończona.")
                        break
                    await asyncio.sleep(0.1)  # Krótkie opóźnienie, aby nie blokować innych operacji

            except Exception as e:
                print(f"Błąd podczas obsługi komunikacji: {e}")

        else:
            print("Nie udało się połączyć z urządzeniem.")

# Uruchomienie funkcji asynchronicznej
if __name__ == "__main__":
    asyncio.run(connect_and_communicate())
