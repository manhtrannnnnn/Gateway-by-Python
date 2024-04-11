import sys
from Adafruit_IO import MQTTClient
import time
import random
from speechRecognition import *
AIO_FEED_IDs = ["led", "waterpump", "speechRecognition"]
AIO_USERNAME = "manhtrannnnnn"
AIO_KEY = "aio_mIXk43QQvph257EfjhmegQkOFqKT"
ledState = 0 
pumpState = 0
speechState = 0

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    global speechState
    global ledState
    global pumpState
    print("Nhan du lieu: " + payload + ", feed_id: " + feed_id)
    if feed_id == "led":
        if payload == "0":
            ledState = 0
            writeData("1")
        else:
            ledState = 1
            writeData("2")
    if feed_id == "waterpump":
        if payload == "0":
            pumpState = 0
            writeData("3")
        else:
            pumpState = 1
            writeData("4")
    # if feed_id == "speechRecognition":
    #     if payload == "ON":  
    #         speechState = 1


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
while True:
    readSerial(client)  
    # if(speechState == 1): 
    #     speech_recognition(client, ledState, pumpState)
    #     speechState = 0
    time.sleep(1)
    # counter = counter - 1
    # if counter <= 0:
    #     counter = 10
    #     soil = random.randint(20,80)
    #     client.publish("earthhumidity", soil)
    #     humi = random.randint(30,100)
    #     client.publish("airhumidity", humi)
    #     lux = random.randint(30,100)
    #     client.publish("light", lux)
    #     tmp = random.randint(30,40)
    #     client.publish("temperature", tmp)
    # time.sleep(1)