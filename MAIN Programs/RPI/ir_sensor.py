from gpiozero import DigitalInputDevice
import config


sensor = DigitalInputDevice(config.IR_GPIO_PIN)

def is_triggered():
    
    return not sensor.value  
