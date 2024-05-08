import sys
from Adafruit_IO import MQTTClient
import time
import json 
from speechRecognition import *
import random
from threading import Thread

AIO_FEED_IDs = ["led", "waterpump", "speechRecognition","color"]
AIO_USERNAME = "manhtrannnnnn"
AIO_KEY = "aio_cEIB30Va6x3dmwHdQd6Lcbv8212N"
ledState = 0 
pumpState = 0
speechState = 0
ledColor = '"white"'
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
    global ledColor
    print("Nhan du lieu: " + payload + ", feed_id: " + feed_id)
    if feed_id == "waterpump":
        if payload == "0":
            pumpState = 0
            writeData("3")
        else:
            pumpState = 1
            writeData("4")
    if feed_id == "led":
        if payload == "0":
            ledState = 0
            writeData("1")
        if payload == "1":
            ledState = 1
            changeColor(ledColor)
    if feed_id == "color":
        ledColor = payload
        if ledState == 1:
            changeColor(ledColor)    
    if feed_id == "speechRecognition":
        if payload == "true":  
            speechState = 1
        elif payload == "false":
            speechState = 0

def changeColor(color):
    if color == '"red"':
        writeData("red")
    elif color == '"orange"':
        writeData("orange")
    elif color == '"yellow"':
        writeData("yellow")
    elif color == '"green"':
        writeData("green")
    elif color == '"blue"':
        writeData("blue")
    elif color == '"purple"':
        writeData("indigo")
    elif color == '"pink"':
        writeData("purple")
    elif color == '"white"':
        writeData("white")
    else: writeData("white")

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()  


def gateway():
    while True:
        readSerial(client)
        time.sleep(1)
thread1 = Thread(target=gateway)
thread1.start()

while True:
    if(speechState == 1):
        speech_recognition(client)
        client.publish("speechRecognition", "false")
        speechState = 0
    