from machine import ADC
from time import sleep
import math

adcPin = 0          # Analog GPIO on Adafruit Feather Huzzah ESP8266
Vcc = 3.3           # Voltage source
#Vref = 1            # ADC reference voltage
#Rth = 10000         # Thermistor resistance
R2 = 33000          # Fixed resistor
adcRes = 1024.0     # ADC resolution (10-bit)

# Steinhart–Hart equation parameters
A = 0.001129148 
B = 0.000234125
C = 0.0000000876741

# Set-up
adc = ADC(adcPin)

while True:
    # 10-bit ADC voltage value
    adcValue = adc.read()
    
    # Thermistor voltage
    Vntc = adcValue / adcRes
    
    # Thermistor resistance
    Rntc = (Vntc * R2) / (Vcc - Vntc)
    
    # Steinhart–Hart equation
    tempK = 1 / (A + (B * math.log(Rntc)) + (C * (math.log(Rntc))**3))
    tempC = tempK - 273.15

    print ('ADC Value: %d, Voltage: %.2f, Temp Celsius: %.2f' %(adcValue,Vntc,tempC))
    sleep(1)


# Notes on building the circuit with Adafruit Feather Huzzah ADC(0) (ESP8266 built-in ADC):
# There are many thermistor labs advocating using 10k fixed resistor with 10k thermistor
# I tried this but the ADC reading was always out of range (always 1024)
# This is because my voltage source is 3V3 but Adafruit Feather Huzzah ADC(0) max input voltage is 1V 
# Ref: https://learn.adafruit.com/adafruit-feather-huzzah-esp8266
# Therefore if powering the thermistor from the Feather Huzzah 3V3 or an external 3V3 power source
# the circuit Voltage needs to be divided from 3V3 to 1V
# One method to do this is via a voltage divider between a fixed resistor and the thermistor
# For our purposes, a fixed resistor greater than 23k will do the job