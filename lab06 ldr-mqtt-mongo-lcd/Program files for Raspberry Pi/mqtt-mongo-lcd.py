#!/usr/bin/python

import paho.mqtt.client as mqtt
import pymongo, pytz, time
from pymongo import MongoClient
from time import sleep, strftime
from datetime import datetime
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')

def init_lcd():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns

def destroy():
    lcd.clear()

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)

# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)


def init_db():
    DB_ENDPOINT = MongoClient('127.0.0.1:27017')
    DB_NAME = "mqtt"
    DB_COLLECTION = "mqtt"
    # Get database connection using database endpoint and name defined above
    global db
    db = DB_ENDPOINT[DB_NAME]
    print ("Database connection: %s" %(db))

def build_dict(message):
    my_tz = pytz.timezone('Australia/Sydney')
    global timestamp
    timestamp = datetime.now(tz=my_tz)

    dict = {
        'Date': timestamp,
        'Sensor': subTopic,
        'Value': message,
    }

#    print ("Sensor data: ", dict)
    return (dict)

def insert_sensor(dict):
    insert_dict = db.mqtt.insert_one(dict)
    return()

def test_db():
    serverStatusResult=db.command("serverStatus")
    print(serverStatusResult)

# Local MQTT server
mqttServer = '127.0.0.1'
# Subscribe topic
subTopic = 'SensorLDR'

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server")
    print('Subscribe to topic %s' %(subTopic))
    client.subscribe(subTopic)

def on_message(client, userdata, message):
#    print("message received " ,str(message.payload.decode("utf-8")))
#    print("message topic=",message.topic)
#    print("message qos=",message.qos)
#    print("message retain flag=",message.retain)
    print(message.payload.decode("utf-8"))
    msg = str(message.payload.decode("utf-8"))
    dict = build_dict(msg)
    insert_sensor(dict)
    lcd.setCursor(0,0)  # set cursor position
    # Display brightness
    lcd.message( 'Brightness: ' + msg +'%\n' )
    # Display current time
#    lcd.message( get_time_now() )
    lcd.message(str(timestamp))

def wait_for(client,msgType,period=0.25):
    if msgType=="SUBACK":
        if client.on_subscribe:
            while not client.suback_flag:
                logging.info("waiting suback")
                client.loop()  #check for messages
                sleep(period)

def init_mqtt():
    # Declare MQTT client
#    print('Instantiate MQTT Client')
    global client
    client = mqtt.Client('rpi4b')  # Create MQTT client instance
    # Connect MQTT client to MQTT server
#    print('Connect to MQTT server %s' %(mqttServer))
    client.connect(mqttServer)    # Connect to MQTT server

def main():
    # Start loop    
#    client.loop_start()    #start the loop

    while True:
        client.on_connect = on_connect
        client.on_message = on_message 
        client.loop_forever()

#    sleep(30) # wait
#    client.loop_stop() #stop the loop

# We need the following for local testing
# Running locally
if __name__ == '__main__':
    init_lcd()
    init_db()
#    test_db()
    init_mqtt()
    main()

