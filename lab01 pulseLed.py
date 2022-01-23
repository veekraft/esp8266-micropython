from machine import Pin, PWM
import time, math

ledPin = 4
blinks = 10
# Time spent at each PWM/brightness level in ms
pulseT = 50

# Set up
led = PWM(Pin(ledPin), freq=1000)

# Define a function to pulse the LED
def pulse(l, t):
	for i in range(20):
		l.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
		time.sleep_ms(t)

for i in range(blinks):
	pulse(led, pulseT)