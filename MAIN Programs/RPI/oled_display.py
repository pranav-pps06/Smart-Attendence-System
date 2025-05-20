import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont


WIDTH = 128
HEIGHT = 64  


i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)


font = ImageFont.load_default()

def display_message(line1="", line2=""):
    
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    draw.text((0, 10), line1, font=font, fill=255)
    draw.text((0, 30), line2, font=font, fill=255)

    
    oled.image(image)
    oled.show()

def display_idle():
    display_message("Waiting", "for IR trigger")

def display_no_control():
    display_message("Disconnected", "from host")

def display_success(name):
    display_message("Attendance", f"Marked: {name}")
