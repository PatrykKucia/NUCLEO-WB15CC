import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)
from bleak import BleakClient

# Adres urządzenia STM32 NUCLEO (zmień na właściwy)
NUCLEO_ADDRESS = "00:80:E1:22:E5:13"

# UUID charakterystyki do zapisu (zmień na właściwy UUID Twojego urządzenia)
WRITE_CHARACTERISTIC_UUID = "00000000-8e22-4541-9d4c-21edae82ed19"  # Przykładowy UUID
NOTIFY_CHARACTERISTIC_UUID = "00001000-8e22-4541-9d4c-21edae82ed19"  # UUID charakterystyki do notyfikacji (zmień na właściwy)

# Funkcja do wypisania dostępnych usług i charakterystyk
async def list_services_and_characteristics(client):
    services = await client.get_services()
    print("Dostępne usługi i charakterystyki:")
    for service in services:
        print(f"Service: {service.uuid}")
        for characteristic in service.characteristics:
            print(f"  Characteristic: {characteristic.uuid}")

# Callback do obsługi notyfikacji
def notification_handler(sender, data):
    print(f"Otrzymano dane z {sender}: {data}")
    
async def connect_and_communicate():
    print(f"Łączenie z urządzeniem {NUCLEO_ADDRESS}...")
    async with BleakClient(NUCLEO_ADDRESS) as client:
        if client.is_connected:
            print("Połączono z urządzeniem STM32 NUCLEO!")

            # Wypisanie dostępnych usług i charakterystyk
            await list_services_and_characteristics(client)

            # Subskrypcja notyfikacji
            try:
                print(f"Subskrypcja notyfikacji na charakterystyce {NOTIFY_CHARACTERISTIC_UUID}...")
                await client.start_notify(NOTIFY_CHARACTERISTIC_UUID, notification_handler)
                print("Subskrypcja aktywna.")

                # Wysłanie danych do urządzenia po subskrypcji
                data_to_send = b"Hello, STM32!"
                print(f"Wysyłanie danych: {data_to_send}")
                await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, data_to_send)
                print("Dane zostały wysłane!")

                # Oczekiwanie na notyfikacje przez 30 sekund
                await asyncio.sleep(30)

                # Wyłączenie notyfikacji
                await client.stop_notify(NOTIFY_CHARACTERISTIC_UUID)
                print("Subskrypcja została zakończona.")
            except Exception as e:
                print(f"Błąd podczas obsługi komunikacji: {e}")

        else:
            print("Nie udało się połączyć z urządzeniem.")

# Uruchomienie funkcji asynchronicznej
if __name__ == "__main__":
    asyncio.run(connect_and_communicate())