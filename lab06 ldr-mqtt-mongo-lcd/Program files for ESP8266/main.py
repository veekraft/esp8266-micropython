import esp, gc
import machine, math
from machine import Pin, PWM, ADC
import network
import time
from time import sleep
import ubinascii
from umqtt.simple import MQTTClient

# Disable debug, enable garbage collection
esp.osdebug(None)
gc.collect()

# Set up for MQTT
mqtt_server = '10.1.1.82'
client_id = ubinascii.hexlify(machine.unique_id())

last_message = 0
message_interval = 5
counter = 0

# Set up for photoresistor
adcP = 0
adcRes = 1024.0
Vcc = 3.3
ldr = ADC(adcP) # light dependent resistor LDR (photoresistor)
topic_pub = b'SensorLDR'

# Set up for LED
ledP = 2
led = PWM(Pin(ledP), freq=1000) # Set PWM frequency to 1kHz
topic_sub = b'ActuateLED'

# Define function
def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'ActuateLED' and msg == b'on':
        print('Edge received actuator %s command' %(str(msg)))
        led.on()
        print('LED should be on now')
    elif topic == b'ActuateLED' and msg == b'off':
        print('Edge received actuator action_off message')
        led.off()
    else:
        print('Nothing to see, move along')

# Define function connect to MQTT broker and subscribe to topic
def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

# Define function microcontroller reset
def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    machine.reset()

# Define function acquire sensor value
def acquire_sensor():
     # Read ADC value
    adcValue = ldr.read()
    # Calculate resistor voltage
    voltage = adcValue/adcRes*Vcc

    # Scale PWM for LED
    pwmDuty = int(adcValue/adcRes*100)
    # Brightness as a percentage, inverse of the PWM Duty Cycle
    bright = 100 - pwmDuty
    
    # Set LED duty cycle
    #led.duty(pwmDuty)
    
    # Print ambient brightness %
    #print('Brightness: %.2f%%' %(bright))
    
    # Print out the ADC value and voltage
    #print('ADC value: %d, PWM: %d Voltage: %.2f' %(adcValue, pwmDuty, voltage))
    sleep(1)
    return(str(bright))
    
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            msg = acquire_sensor()
            client.publish(topic_pub, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()