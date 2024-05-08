import serial.tools.list_ports

class UARTData:
    tmp = ""
    humi = ""
    soil = ""
    light = ""

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"   
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

if getPort() != "None":
  ser = serial.Serial( port=getPort(), baudrate=115200)
  print(ser)

def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    UARTData.tmp = splitData[1]
    UARTData.humi = splitData[3]
    UARTData.soil = splitData[5]
    UARTData.light = splitData[7]
    if splitData[0] == "TEMP":
        client.publish("temperature", UARTData.tmp)
    if splitData[2] == "HUMI":
        client.publish("airhumidity", UARTData.humi)
    if splitData[4] == "SOIL":
        client.publish("earthhumidity", UARTData.soil)
    if splitData[6] == "LIGHT": 
        client.publish("light", UARTData.light)       

mess = ""

def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def writeData(data):
    ser.write(str(data).encode())