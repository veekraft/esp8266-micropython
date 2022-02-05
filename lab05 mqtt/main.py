import machine
import math
import time
import umqtt.simple

# Set up for MQTT
mqtt_server = '10.1.1.82'
client_id = umqtt.simple.hexlify(machine.unique_id())
topic_sub = b'ActuatorLED'
topic_pub = b'SensorNTC'
last_message = 0
message_interval = 5
counter = 0

# Set up for ntc thermistor
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

# Define callback function
def sub_cb(topic, msg):
    global topic_sub
    print((topic, msg))
    if topic == topic_sub and msg == b'on':
        led.on()
        print('LED on')
    elif topic == b'ActuatorLED' and msg == b'off':
        led.off()
        print('LED off')
    else:
        print('Nothing to see, move along')

# Define function connect to MQTT broker and subscribe to topic
def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = umqtt.simple.MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to MQTT server: %s' % (mqtt_server))
    client.subscribe(topic_sub)
    print('Subscribed to topic: %s' % (topic_sub))
    return client

# Define function microcontroller reset
def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

# Define function acquire sensor value
def acquire_sensor():
    sensor = 'ntc'
    adcValue = adc.read()
    Vntc = adcValue / adcRes
    Rntc = (Vntc * R2) / (Vcc - Vntc)
    temp = (1 / (A + (B * math.log(Rntc)) + (C * (math.log(Rntc))**3))) - 273.15
    msg = (sensor + ':' + str(temp))
    print(msg)
    return msg

# Establish connection to broker, subscribe to topic
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

# Check for topic update, publish sensor reading 
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