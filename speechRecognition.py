import speech_recognition as sr
import pyttsx3
from uart import *
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)


def voice_talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    voice = sr.Recognizer()
    with sr.Microphone() as mic:
        print("I am listening...")
        audio = voice.record(mic, duration=5)
    try:
        text = voice.recognize_google(audio, language="vi")
        text = text.split()
        print(text)
    except:
        text = 'Can not recognize'
    return text


def reply(client, text):
    if any(word in text for word in ["đèn", "lamp", "light"]):
        if any(word in text for word in ["tắt", "off"]):
            client.publish("led", "0")
            voice_talk('The light is turned off')
        elif any(word in text for word in ["bật", "on"]):
            client.publish("led", "1")
            voice_talk('The light is turned on')
    elif any(word in text for word in ["bơm", "pump", "turn"]):
        if any(word in text for word in ["tắt", "off"]):
            client.publish("waterpump", "0")
            voice_talk('The pump is turned off')
        elif any(word in text for word in ["bật", "on"]):
            client.publish("waterpump", "1")
            voice_talk('The pump is turned on')
    elif any(word in text for word in ["temperature", "nhiệt độ"]):
        voice_talk("The temperature is " + str(UARTData.tmp) + " degrees Celsius")
    elif any(word in text for word in ["humidity", "không khí"]):
        voice_talk('The humidity level is ' + str(UARTData.humi) + ' percent')
    elif any(word in text for word in ["light intensity", "ánh sáng"]):
        voice_talk('The light intensity is ' + str(UARTData.light) + ' lux')
    elif any(word in text for word in ["soil", "độ đất"]):
        voice_talk('The soil moisture is ' + str(UARTData.soil) + ' percent')
    elif "recognize" in text:
        return
    else:
        voice_talk("Can you say that again?")
        return


def speech_recognition(client):
    voice_talk('How can I help you?')
    while True:
        text = listen()
        if any(word in text for word in ["thank", "cảm", "ơn"]):
            voice_talk("You're welcome. Have a nice day!")
            break
        else:
            reply(client, text)

