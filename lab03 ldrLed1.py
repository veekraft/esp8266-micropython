from machine import Pin, Signal, PWM, ADC
from time import sleep_ms

ledP = 4
adcP = 0

led = PWM(Pin(ledP), freq=1000) # Set PWM frequency to 1kHz
ldr = ADC(adcP) # light dependent resistor LDR (photoresistor)

while True:
    # Read photoresistor value
    value = ldr.read()
    voltage = value/1024.0*3.3
   
    # Set LED duty cycle based on photoresistor value
    led.duty(int(value/1024*100))
   
    # Print out the photoresistor value and voltage
    print('Photoresistor value: %d, Voltage: %.2f' %(value, voltage))
    sleep_ms(10)