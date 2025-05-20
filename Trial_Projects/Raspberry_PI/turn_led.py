import time
import requests
import logging
from gpiozero import LED
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# ==== CONFIGURATION ====
PC_SERVER_URL = 'http://192.168.66.182:5000/status'  # <-- Replace with your actual IP
LED_PIN = 18

# ==== LOGGING SETUP ====
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==== LED SETUP ====
led = LED(LED_PIN)

# ==== OLED SETUP ====
WIDTH = 128
HEIGHT = 32  # Use 64 if your OLED is 128x64

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)
oled.show()

def display_status(message):
    """Display a message on the OLED."""
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((0, 0), message, font=font, fill=255)
    oled.image(image)
    oled.show()

def set_led(state):
    """Turn LED on or off based on state."""
    if state == 'on':
        led.on()
    else:
        led.off()

def main():
    last_status = None
    while True:
        try:
            response = requests.get(PC_SERVER_URL, timeout=2)
            status = response.text.strip().lower()
            logging.info(f"Received status: {status}")

            if status not in ['on', 'off']:
                display_status("UNKNOWN STATUS")
                logging.warning("Received unknown status from server.")
                continue

            if status != last_status:
                set_led(status)
                display_status(f"LED is {status.upper()}")
                last_status = status

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            display_status("CONN ERROR")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            display_status("ERROR")

        time.sleep(2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Interrupted by user.")
    finally:
        oled.fill(0)
        oled.show()
        logging.info("Cleaned up OLED.")
