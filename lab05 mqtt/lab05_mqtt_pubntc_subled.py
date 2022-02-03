import esp
import gc
import machine
import math
import micropython
import network
import ubinascii
import time
from umqttsimple import MQTTClient

# Disable debug, enable garbage collection
esp.osdebug(None)
gc.collect()

# Set up for MQTT
mqtt_server = '10.1.1.82'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'ActuatorActivation'
topic_pub = b'SensorReading'
last_message = 0
message_interval = 5
counter = 0

# Set up for thermistor
adcPin = 0
Vcc = 3.3
R2 = 33000
adcRes = 1024.0
A = 0.001129148 
B = 0.000234125
C = 0.0000000876741
adc = machine.ADC(adcPin)

# Set up for LED
ledPin = 4
led = machine.Signal(ledPin, machine.Pin.OUT, invert=False)

# Define function
def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'ActuatorActivation' and msg == b'on':
        print('Edge received actuator %s command' %(str(msg)))
        led.on()
        print('LED should be on now')
    elif topic == b'ActuatorActivation' and msg == b'off':
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
    time.sleep(10)
    machine.reset()

# Define function acquire sensor value
def acquire_sensor():
    sensor = 'Temperature'
    adcValue = adc.read()
    Vntc = adcValue / adcRes
    Rntc = (Vntc * R2) / (Vcc - Vntc)
    temp = (1 / (A + (B * math.log(Rntc)) + (C * (math.log(Rntc))**3))) - 273.15
    return str(temp)

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