import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL, board.SDA)

WIDTH = 128
HEIGHT = 64  

oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

oled.fill(0)
oled.show()

image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)  
draw.text((0, 0), "Hello, OLED!", font=font, fill=255)
draw.text((0, 16), "0.98 inch SSD1306", font=font, fill=255)

oled.image(image)
oled.show()

time.sleep(10)

oled.fill(0)
oled.show()
