import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import pyttsx3
from uart import *
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
def voice_talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
  voice = sr.Recognizer()
  with sr.Microphone() as mic:
    print("i am listening.........")
    audio = voice.record(mic, duration=5)
  try:
    text = voice.recognize_google(audio, language = "vi")
    text = text.split()
    print(text) 
  except:
    text = 'Can not recognize'
  return text

def reply(client,text,ledState,pumpState):
    if "đèn" in text or "lamp" in text or "Đèn" in text or "Lamp" in text or "light" in text or "Light" in text:
      if "tắt" in text or "off" in text or "Tắt" in text or "Off" in text:
        if(ledState == 0): voice_talk('The light is already turn off')
        else :
          client.publish("led", "0")
          voice_talk('The light is turn off')
        return
      elif "bật" in text or "on" in text or "Bật" in text or "On" in text:
        if(ledState == 1): voice_talk('The light is already turn on')
        else: 
          client.publish("led", "1")
          voice_talk('The light is turn on')
        return
    elif "bơm" in text or "pump" in text or "Bơm" in text or "Pump" in text or "turn" in text or "Turn" in text:
      if "tắt" in text or "off" in text or "Tắt" in text or "Off" in text:
        if(pumpState == 0): voice_talk('The pump is already turn off')
        else: 
          client.publish("waterpump", "0")
          voice_talk('The pump is turn off')
        return
      elif "bật" in text or "on" in text or "Bật" in text or "On" in text:
        if(pumpState == 1): voice_talk('The pump is already turn on')
        else:
          client.publish("waterpump", "1")
          voice_talk('The pump is turn on')
        return
    elif "temperature" in text or ("nhiệt" in text and "độ" in text):
        string = "The temperature is " + str(UARTData.tmp) + " degrees Celsius"
        voice_talk(string)
        return
    elif "humidity" in text or ("không" in text and "khí" in text):  
        voice_talk('The humidity level is' + str(UARTData.humi) + 'percent')
        return
    elif "light" in text or  ("ánh" in text and "sáng" in text):
        voice_talk('The light intensity is ' + str(UARTData.light) + ' lux')
        if(int(UARTData.light) < 40 and ledState == 0):
           voice_talk('The light intensity is too weak and the light is not turned on. Do you want to turn on the light')
           text = listen()
           if "yes" in text or "Yes" in text or "on" in text or "On" in text or "bật" in text or "Bật" in text: 
              client.publish("led", "1")
              voice_talk('The led is turn on')
           else:        
              voice_talk('You should check your garden')
        elif(int(UARTData.light) > 100 and ledState == 1):
            voice_talk('The light intensity is quite high and the light is turned on. Do you want to turn off the light')
            text = listen()
            if "Yes" in text or "yes" in text or "off" in text or "Off" in text or "tắt" in text or "Tắt" in text:
              client.publish("led","0")
              voice_talk("The led is turn off")
            else:
              voice_talk('You should check your garden')
        return
    elif "soil" in text or ("độ" in text and "đất" in text):
        voice_talk('The soil moisture is' + str(UARTData.soil) + 'percent')
        if(int(UARTData.soil) < 20 and pumpState == 0):
           voice_talk("The soil moisture is slightly low and the pump is not turned on. Do you want to turn on the pump")
           text = listen()
           if "yes" in text or "Yes" in text or "on" in text or "On" in text or "bật" in text or "Bật" in text:
              client.publish("waterpump", "1")
              voice_talk('The pump is turn on')
           else:
              voice_talk('You should check your garden')
        elif(int(UARTData.soil) > 70 and pumpState == 1):
           voice_talk('The soil moisture is slightly high and the pump is turned on. Do you want to turn off the pump')
           text = listen()
           if "Yes" in text or "yes" in text or "off" in text or "Off" in text or "tắt" in text or "Tắt" in text:
              client.publish("waterpump", "0")
              voice_talk("The pump is turn off")
           else:
              voice_talk('You should check your garden')         
        return
    else:
      return  
    
def speech_recognition(client,ledState,pumpState):
    text = listen()
    reply(client,text,ledState,pumpState)
# def speech_recognition(client, ledState, pumpState):
#   voice = sr.Recognizer()
#   with sr.Microphone() as mic:
#     print("i am listening.........")
#     audio = voice.record(mic, duration=5)
#   try:
#     text = voice.recognize_google(audio, language = "vi")
#     text = text.split()
#     print(text)
#     if "đèn" in text or "lamp" in text or "Đèn" in text or "Lamp" in text or "light" in text or "Light" in text:
#       if "tắt" in text or "off" in text or "Tắt" in text or "Off" in text:
#         if(ledState == 0): voice_talk('The light is already turn off')
#         else :
#           client.publish("led", "0")
#           voice_talk('The light is turn off')
#         return
#       elif "bật" in text or "on" in text or "Bật" in text or "On" in text:
#         if(ledState == 1): voice_talk('The light is already turn on')
#         else: 
#           client.publish("led", "1")
#           voice_talk('The light is turn on')
#         return
#     elif "bơm" in text or "pump" in text or "Bơm" in text or "Pump" in text or "turn" in text or "Turn" in text:
#       if "tắt" in text or "off" in text or "Tắt" in text or "Off" in text:
#         if(pumpState == 0): voice_talk('The pump is already turn off')
#         else: 
#           client.publish("waterpump", "0")
#           voice_talk('The pump is turn off')
#         return
#       elif "bật" in text or "on" in text or "Bật" in text or "On" in text:
#         if(pumpState == 1): voice_talk('The pump is already turn on')
#         else:
#           client.publish("waterpump", "1")
#           voice_talk('The pump is turn on')
#         return
#     elif "temperature" in text or ("nhiệt" in text and "độ" in text):
#         string = "The temperature is " + str(UARTData.tmp) + " degrees Celsius"
#         voice_talk(string)
#         return
#     elif "humidity" in text or ("không" in text and "khí" in text):
#         voice_talk('The humidity level is' + str(UARTData.humi) + 'percent')
#         return
#     elif "light" in text or  ("ánh" in text and "sáng" in text):
#         voice_talk('The light intensity is ' + str(UARTData.light) + ' lux')
#         return
#     elif "soil" in text or ("độ" in text and "đất" in text):
#         voice_talk('The soil moisture is' + str(UARTData.soil) + 'percent')
#         return
#     else:
#       return  
#   except:
#     text = "Cant recognize"