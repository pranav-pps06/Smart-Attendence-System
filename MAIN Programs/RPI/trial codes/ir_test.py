from gpiozero import DigitalInputDevice
import time


IR_GPIO_PIN = 17  


sensor = DigitalInputDevice(IR_GPIO_PIN)

print("IR sensor test started. Press Ctrl+C to exit.")

try:
    while True:
        if sensor.value == 0:
            print("?? IR Triggered (Obstacle Detected)")
        else:
            print("?? IR Clear (No Obstacle)")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Test stopped.")
