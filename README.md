# NUCLEO-WB15CC

## Testing STM32WB15CC
![alt text](image.png)
---

## Spis treści
1. [Schematic](#Schematic)
2. [Useful links](#Useful_links)
4. [Useful videos](#Useful_videos)
5. [Pinout](#Pinout)
6. [Functions](#Functions)
7. [Terminology and theory](#Terminology_and_theory)
8. [Codes](#Codes)
---

## Schematic

![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)


[File with schematic](Datasheets/schemat.pdf)

---

## Useful_links

- [ST page](https://www.st.com/en/evaluation-tools/nucleo-wb15cc.html)

- [BLE w robotyce](https://www.stm32wrobotyce.pl/2023/12/08/ble-1-wprowadzenie-do-bluetooth-low-energy)

---

## Useful_videos

- [ST Getting Started](https://www.youtube.com/watch?v=7_wBH7mTQ2g&list=PLnMKNibPkDnG9JRe2fbOOpVpWY7E4WbJ-&index=1)
---

## Pinout
![alt text](image-5.png)
![alt text](image-4.png)
![alt text](image-6.png)
![alt text](image-7.png)
---

## Functions

---

## Terminology and theory
HSEM - Hardware semaphore wich is used to synchronize access to shared resources between CM0+ and CM4 cores.
 
IPCC - Interprocessor communication controller is used to exchange data between CM0+ and CM4 cores.

GATT - Generic Attribute Profile is API for BLE communication.

GATT terminology:
- Client - A device that initiates GATT commands and requests, and accepts responses, for example, a computer or smartphone.
- Server - A device that receives GATT commands and requests, and returns responses, for example, a temperature sensor.
- Characteristic - A data value transferred between client and server, for example, the current battery voltage.
- Service - A collection of related characteristics, which operate together to perform a particular function. For instance, the Health Thermometer service includes characteristics for a temperature measurement value, and a time interval between measurements.
- Descriptor - A descriptor provides additional information about a characteristic. For instance, a temperature value characteristic may have an indication of its units (e.g. Celsius), and the maximum and minimum values which the sensor can measure. Descriptors are optional – each characteristic can have any number of descriptors.
- Identifier - Services, characteristics, and descriptors are collectively referred to as attributes, and identified by UUIDs. Any implementer may pick a random or pseudorandom UUID for proprietary uses, but the Bluetooth SIG have reserved a range of UUIDs (of the form xxxxxxxx-0000-1000-8000-00805F9B34FB[55]) for standard attributes. For efficiency, these identifiers are represented as 16-bit or 32-bit values in the protocol, rather than the 128 bits required for a full UUID. For example, the Device Information service has the short code 0x180A, rather than 0000180A-0000-1000-... . The full list is kept in the Bluetooth Assigned Numbers (https://www.bluetooth.com/specifications/assigned-numbers/) document online.

| Function              | Bluetooth Low Energy                | Bluetooth Classic                       |
|-----------------------|--------------------------------------|-----------------------------------------|
| Energy Consumption    | Optimized for low energy consumption, making it ideal for battery-powered devices such as IoT or health monitoring devices. | Characterized by higher energy consumption, which can be problematic for battery-powered devices. |
| Data Transfer         | Has lower data throughput compared to Bluetooth Classic. It is more optimized for sending small amounts of data over short periods. | Has higher data throughput, making it more suitable for applications requiring the transfer of larger amounts of data, such as audio transmission. |
| Protocol Structure    | Has a simpler protocol structure, which makes implementation easier and reduces resource overhead. | More complex in terms of protocol structure, which may require a greater amount of system resources. |
| Connections           | Features faster connection establishment, which is beneficial for applications requiring immediate response. | The connection establishment process can be more time-consuming compared to BLE. |
| Number of Channels in the 2.4 GHz Band | Utilizes 40 channels with a bandwidth of 2 MHz. Three of them are used for advertising mode. | Utilizes 79 channels with a bandwidth of 1 MHz. 32 of these are used for advertising. |

---

## Codes

- BLE_TransparentMode - Example of BLE communication in transparent mode.
