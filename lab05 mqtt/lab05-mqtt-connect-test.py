import machine
import time
import umqtt.simple

mqtt_server = '10.1.1.82'
client_id = umqtt.simple.hexlify(machine.unique_id())
topic_sub = b'ActuatorLED'
topic_pub = b'SensorNTC'
last_message = 0
message_interval = 5
counter = 0

def sub_cb(topic, msg):
    global topic_sub
    print((topic, msg))
    if topic == topic_sub and msg == b'on':
        print('Received command for actuator: %s' %(str(msg)))
        # print('LED: %s', %(str(msg)))
        
def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = umqtt.simple.MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to MQTT server: %s' % (mqtt_server))
    client.subscribe(topic_sub)
    print('Subscribed to topic: %s' % (topic_sub))
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
        print('checking for new msg')
        client.check_msg()
        print('publishing new msg')
        client.publish(topic_pub, 'hi there')
        time.sleep(5)
    except OSError as e:
        restart_and_reconnect()