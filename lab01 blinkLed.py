from machine import Pin, Signal
from time import sleep

ledPin = 4
blinks = 5
sleepT = 1

# Set up
led = Signal(ledPin, Pin.OUT, invert=False)

# Blink the LED "blinks" times

for i in range(blinks):
    led.on()
    sleep(sleepT)
    led.off()
    sleep(sleepTime)