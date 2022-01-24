from machine import ADC
from time import sleep
import math

adcPin = 0          # Analog GPIO on Adafruit Feather Huzzah ESP8266
Vcc = 3.3           # Reference Voltage
#R1 = 10000         # 10k thermistor
R2 = 150000         # Fixed resistor
adcRes = 1024.0     # ADC 10-bit resolution

# Steinhart–Hart equation parameters
A = 0.001129148 
B = 0.000234125
C = 0.0000000876741

# Set-up
adc = ADC(adcPin)

while True:
    # 10-bit analog voltage value
    adcValue = adc.read()
    
    # Thermistor voltage drop
    Vntc = adcValue / adcRes
    
    # Thermistor resistance
    Rntc = (Vntc * R2) / (Vcc - Vntc)
    
    # Steinhart–Hart equation
    tempK = 1 / (A + (B * math.log(Rntc)) + (C * (math.log(Rntc))**3))
    tempC = tempK - 273.15

    print ('ADC Value: %d, Voltage: %.2f, Temp Celsius: %.2f' %(adcValue,Vntc,tempC))
    sleep(1)


# Notes on the circuit:
# There are many thermistor labs advocating using 10k fixed resistor with 10k thermistor
# I tried these, both with thermistor hooked high and low but both produced ADC reading out of range (always 1024)
# no matter what the ambient temperature
# This code works for a circuit with fixed 150k resistor pulled up to 3.3V, thermistor is pulled down to Ground