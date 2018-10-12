#!/usr/bin/env python3
import serial
import paho.mqtt.client as mqtt

broker = ""
port = 1883
statustopic = "raspberry/gps/status"

client = mqtt.Client("RpiGPS")
client.connect(broker, port=port)

try:
    print("Connecting to serial...")
    gps = serial.Serial("/dev/ttyACM0",9600)
    print("Retrieving data...")
    line = gps.readline
    data = line.split(",")
    client.publish(statustopic, "Online")
    if data[0] == "$GPGGA":
        latitude = data[2]
        longitude = data[4]
        #Fix Quality: 0-invalid, 1-GPS, 2-DGPS
        quality = data[6]
        numberofsatellites = data[7]
        altitude = data[9]
    print("Data received!")

    for element in data:
        print(element)

except:
    print("Unable to connect to serial device!")
    client.publish(statustopic, "Offline")

client.disconnect()
