import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)
from bleak import BleakClient

# Adres urządzenia STM32 NUCLEO (zmień na właściwy)
NUCLEO_ADDRESS = "00:80:E1:22:E5:13"

# UUID charakterystyki do zapisu (zmień na właściwy UUID Twojego urządzenia)
WRITE_CHARACTERISTIC_UUID = "00000000-8e22-4541-9d4c-21edae82ed19"  # Przykładowy UUID

# Funkcja do wypisania dostępnych usług i charakterystyk
async def list_services_and_characteristics(client):
    services = await client.get_services()
    print("Dostępne usługi i charakterystyki:")
    for service in services:
        print(f"Service: {service.uuid}")
        for characteristic in service.characteristics:
            print(f"  Characteristic: {characteristic.uuid}")

# Funkcja do połączenia z urządzeniem i wysłania danych
async def connect_and_send():
    print(f"Łączenie z urządzeniem {NUCLEO_ADDRESS}...")
    async with BleakClient(NUCLEO_ADDRESS) as client:
        if client.is_connected:
            print("Połączono z urządzeniem STM32 NUCLEO!")

            # Wypisanie dostępnych usług i charakterystyk
            await list_services_and_characteristics(client)

            # Dane do wysłania (zmień na dane, które chcesz wysłać)
            data_to_send = b"Hello, STM32!"
            print(f"Wysyłanie danych: {data_to_send}")

            # Zapis danych do charakterystyki
            try:
                await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, data_to_send)
                print("Dane zostały wysłane!")
            except Exception as e:
                print(f"Błąd przy wysyłaniu danych: {e}")

        else:
            print("Nie udało się połączyć z urządzeniem.")

# Uruchomienie funkcji asynchronicznej
if __name__ == "__main__":
    asyncio.run(connect_and_send())
