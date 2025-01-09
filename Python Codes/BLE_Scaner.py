import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)
from bleak import BleakClient

# Adres urządzenia STM32 NUCLEO (zmień na właściwy)
NUCLEO_ADDRESS = "00:80:E1:22:E5:13"

# UUID charakterystyki do zapisu (zmień na właściwy UUID Twojego urządzenia)
WRITE_CHARACTERISTIC_UUID = "00000000-CC7A-482A-984A-7F2ED5B3E58F"  # Przykładowy UUID

# Funkcja do połączenia z urządzeniem i wysłania danych
async def connect_and_send():
    print(f"Łączenie z urządzeniem {NUCLEO_ADDRESS}...")
    async with BleakClient(NUCLEO_ADDRESS) as client:
        if client.is_connected:
            print("Połączono z urządzeniem STM32 NUCLEO!")

            # Dane do wysłania (zmień na dane, które chcesz wysłać)
            data_to_send = b"Hello, STM32!"
            print(f"Wysyłanie danych: {data_to_send}")

            # Zapis danych do charakterystyki
            await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, data_to_send)
            print("Dane zostały wysłane!")

        else:
            print("Nie udało się połączyć z urządzeniem.")

# Uruchomienie funkcji asynchronicznej
if __name__ == "__main__":
    asyncio.run(connect_and_send())
