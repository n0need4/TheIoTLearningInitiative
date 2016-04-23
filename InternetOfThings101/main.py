#!/usr/bin/python

import paho.mqtt.client as paho
import psutil
import pywapi
import signal
import sys
import time
import uuid

from threading import Thread

def interruptHandler(signal, frame):
    sys.exit(0)

def on_publish(mosq, obj, msg):
    pass

def dataNetwork():
    netdata = psutil.net_io_counters()
    return netdata.packets_sent + netdata.packets_recv
from uuid import getnode as get_mac

def dataNetworkHandler():
    idDevice = str(get_mac)
    mqttclient = paho.Client()
    mqttclient.on_publish = on_publish
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    while True:
        packets = dataNetwork()
        message = idDevice + " " + str(packets)
        print "dataNetworkHandler " + message
        mqttclient.publish("IoT101/Network", message)
        time.sleep(1)

def on_message(mosq, obj, msg):
    print "dataMessageHandler %s %s" % (msg.topic, msg.payload)

def dataMessageHandler():
    mqttclient = paho.Client()
    mqttclient.on_message = on_message
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/Message", 0)
    while mqttclient.loop() == 0:
        pass

def dataWeatherHandler():
    weather = pywapi.get_weather_from_yahoo('MXJO0043', 'metric')
    message = "Weather Report in " + weather['location']['city']
    message = message + ", Temperature " + weather['condition']['temp'] + " C"
    message = message + ", Atmospheric Pressure " + weather['atmosphere']['pressure'] + " mbar"
    print message

if __name__ == '__main__':

    signal.signal(signal.SIGINT, interruptHandler)

    threadx = Thread(target=dataNetworkHandler)
    threadx.start()

    threadx = Thread(target=dataMessageHandler)
    threadx.start()

    dataWeatherHandler()

    while True:
        print "Hello Internet of Things 101"
        time.sleep(5)

# End of File
