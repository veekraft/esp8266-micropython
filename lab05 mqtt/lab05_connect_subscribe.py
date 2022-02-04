import machine
import time
import ubinascii
from umqttsimple import MQTTClient

mqtt_server = '10.1.1.82'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'ActuatorActivation'
last_message = 0
message_interval = 5
counter = 0

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'HELLO' and msg == b'hello':
        print('We got a %s from MQTT' %(str(msg)))
    else:
        print('Nothing to see, move along')
        
def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
    except OSError as e:
        restart_and_reconnect()