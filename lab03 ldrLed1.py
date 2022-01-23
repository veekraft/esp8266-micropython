from machine import Pin, Signal, PWM, ADC
from time import sleep_ms

ledP = 4
adcP = 0

led = PWM(Pin(ledP), freq=1000) # Set PWM frequency to 1kHz
ldr = ADC(adcP) # light dependent resistor LDR (photoresistor)

while True:
    # Read ADC value
    value = ldr.read()
    # Calculate voltage
    voltage = value/1024.0*3.3
    # Scale PWM for LED
    pwmDuty = int(value/1024*100)
    
    # Set LED duty cycle
    led.duty(pwmDuty)
   
    # Print out the ADC value and voltage
    print('ADC value: %d, PWM: %d Voltage: %.2f' %(value, pwmDuty, voltage))
    sleep_ms(10)