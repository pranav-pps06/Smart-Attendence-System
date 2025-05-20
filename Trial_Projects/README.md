# 💡 Smart LED ON/OFF System
## 📋 Description
This project demonstrates a **local-network-based IoT system** using a **Raspberry Pi**, where a **LED and an OLED display** are controlled from a **PC** through a Flask web application. While it doesn't use the internet, it mimics an IoT system architecture using a LAN.
> **Note:** This is technically not a full IoT implementation since it operates over a local network only.

---
## 🧰 Requirements

- 🖥️ PC or Laptop (connected to the same local network)
- 🍓 Raspberry Pi (with GPIO access)
- 💡 LED (connected to Raspberry Pi GPIO)
- 🧾 OLED display (I2C-based, like SSD1306)
- 🔗 Local network (Wi-Fi or Ethernet)
- 📦 Required software and Python packages (see below)

---
## 🛠️ Setup Instructions

### 🧾 Step 1: Set Up Raspberry Pi

#### 1.1. Install system dependencies:
```bash
sudo apt update
sudo apt install -y python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential \
                    libopenjp2-7 libtiff5 libatlas-base-dev i2c-tools python3-pil
```
#### 1.2. Enable I2C interface:
``` bash
sudo raspi-config
```
Interface Options → I2C → Enable <br/> Then reboot:
``` bash
sudo reboot
```
#### 1.3. Create and activate a virtual environment:
```bash
python3 -m venv ~/basics
source ~/basics/bin/activate
```
#### 1.4. Install Python packages:
```bash
pip install --upgrade pip
pip install gpiozero requests adafruit-blinka adafruit-circuitpython-ssd1306
```
#### 1.5. Download and place the control script:
Download the turn_led.py script and place it in your home directory:

---
### 💻 Step 2: Set Up PC (Web Control Panel)
#### 2.1. Create project folder and navigate into it:
```bash
mkdir smart-led-control
cd smart-led-control
```
#### 2.2. Set up and activate a virtual environment:
```bash
python3 -m venv venv
```
Activate the environment:
```bash
venv\Scripts\Activate.ps1
```
#### 2.3. Install required Python libraries:
```bash
pip install flask requests
```
#### 2.4. Create project structure:
```bash
smart-led-control/
│
├── app.py               # Flask backend
├── venv/                # Virtual environment
└── templates/
    └── index.html       # Web control UI
```
Place your index.html inside the templates/ folder and your app.py at the root.
#### 2.5. Run the Flask server:
```bash
python app.py
```
>The server will start (e.g., at http://192.168.0.100:5000/). This IP is what your Raspberry Pi needs to contact.
---
### 🔌 Step 3: Run the Raspberry Pi Script
On your Raspberry Pi:
```basics
source ~/basics/bin/activate
python turn_led.py
```
This script will repeatedly poll your PC's Flask server every few seconds and turn the LED on or off based on the web UI.

---
## 🌐 How It Works
- The PC runs a Flask server that hosts a simple UI to toggle the LED status (ON or OFF).
- The Raspberry Pi continuously polls this server's /status endpoint.
- Based on the returned value (on or off), the Pi turns the LED on/off and updates the OLED display with the current status.

---
## 🚨 Notes
- Ensure both the PC and Raspberry Pi are on the same network.
- Make sure to update the PC_SERVER_URL in turn_led.py to reflect your PC's IP address.
- Use i2cdetect -y 1 on the Raspberry Pi to confirm the OLED is detected on I2C.

---
## 🏁 Future Improvements
- Add bi-directional communication using WebSockets.
- Use MQTT or external broker for full IoT functionality.
- Add multiple device support or a dashboard view.

---
