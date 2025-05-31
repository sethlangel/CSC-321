# RFID Security Test Bench (MicroPython + Raspberry Pi Pico)

This project demonstrates the security vulnerabilities of UID based RFID authentication using a Raspberry Pi Pico and an MFRC522 RFID reader. It allows users to read and write RFID tags, log access attempts, simulate spoofing, and explore security improvements for RFID based access systems.

---

## Features

- Read/write RFID tags using MFRC522
- Green/Red LEDs for visual access indication
- Access control via authorized UID list
- Logs events with timestamp, tag ID, and access status
- Designed for use with MicroPython and the VSCode plugin
- Extendable for physical lock control and multi-factor authentication

---

## Hardware Required

| Component               | Quantity |
|------------------------|----------|
| Raspberry Pi Pico      | 1        |
| MFRC522 RFID Module    | 1        |
| RFID Tags/Cards        | 2 or more |
| LEDs (Green and Red)   | 2        |
| 330Ω Resistors         | 2        |
| Jumper Wires           | As needed |
| Breadboard             | 1        |

---

## Hardware Setup

### Overview

The project uses a Raspberry Pi Pico connected to an MFRC522 RFID module via SPI (Serial Peripheral Interface), along with two LEDs to visually indicate access status (green for granted, red for denied). The entire system can be built on a breadboard for prototyping and testing.

### GPIO Pin Usage

| Component        | Pico GPIO | Description           |
|------------------|-----------|-----------------------|
| MFRC522 SDA      | GP17      | SPI Chip Select       |
| MFRC522 SCK      | GP18      | SPI Clock             |
| MFRC522 MOSI     | GP19      | SPI Master Out        |
| MFRC522 MISO     | GP16      | SPI Master In         |
| MFRC522 RST      | GP9       | Reset pin             |
| Green LED        | GP14      | Access Granted LED    |
| Red LED          | GP15      | Access Denied LED     |

> **Note**: The MFRC522 requires 3.3V power — do not connect it to 5V or you risk damaging your Pico or the RFID module.

---

### Step-by-Step Assembly

1. **Place your Raspberry Pi Pico on a breadboard** so each side has accessible rows.
2. **Connect the MFRC522 module**:
   - Wire SDA, SCK, MOSI, MISO, RST, 3.3V, and GND to the correct Pico pins (see table above).
3. **Connect the LEDs**:
   - Connect the anode (longer leg) of each LED to its GPIO pin via a 330Ω resistor.
   - Connect the cathode (shorter leg) to GND.
4. **Double-check power and ground lines**: Ensure that all components share the same GND and that the RFID module is powered via the Pico’s 3.3V pin.
5. **Test continuity or loose wires**: Poor breadboard connections are a common issue during prototyping.

---

### Wiring Diagram

![Untitled Sketch 2_bb](https://github.com/user-attachments/assets/00a527aa-462d-4517-864e-20a2e1bc6b97)

---

### Optional Hardware Extensions

- **Servo Motor (for future door lock control)**: Connect signal to a free GPIO (e.g., GP13), powered externally.
- **Keypad Matrix**: Useful for adding PIN-based multi-factor authentication.
- **OLED Display**: To show access logs or current status.

---

## Software Setup

### Tools Required

- [Visual Studio Code (VSCode)](https://code.visualstudio.com/)
- [MicroPico VSCode Extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go)
- MicroPython firmware for Raspberry Pi Pico
- USB cable to connect your Pico

---

### Step 1: Flash MicroPython Firmware on the Pico

1. Hold the **BOOTSEL** button on your Pico and plug it into your PC.
2. Your Pico will mount as a USB drive called `RPI-RP2`.
3. Download the latest `.uf2` firmware for **MicroPython on Raspberry Pi Pico** from [official site](https://micropython.org/download/rp2-pico/).
4. Drag and drop the `.uf2` file into the `RPI-RP2` drive.
5. Pico will reboot and appear as a serial device.

---

### Step 2: Set Up VSCode for MicroPython

1. Launch **VSCode**.
2. Install the **MicroPython extension** from the Extensions Marketplace.
3. Open the **Command Palette** and select **MicroPico: Initialize MicroPico Project**
4. Choose **Raspberry Pi Pico** and select the serial port for your device.
5. The REPL should now be available at the bottom.

---

### Step 3: Upload Files to Pico
1. Clone the project repository.
2. Open the **Command Palette** and select **MicroPico: Upload Project to Pico**.
3. Click **Play Button** in the bottom left corner in VS Code to run the project on your Pico.
