#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
import paho.mqtt.client as mqtt
import json

CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883

try:
     config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
except :
     config = None

remote_mqtt = mqtt.Client()
remote_mqtt.connect(config.get('secret').get('remote-mqtt-host'), int(config.get('secret').get('remote-mqtt-port')))

local_mqtt = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print 'Connected'
    client.subscribe('hermes/tts/say')

def on_disconnect(client, userdata, rc):
    print 'Disconnected'

def on_message(client, userdata, msg):
    if msg.topic == 'hermes/tts/say':
        rc = remote_mqtt.publish(msg.topic, msg.payload)
        rc.wait_for_publish()
        if rc.is_published:
            print 'Published : {} - {}'.format(msg.topic, msg.payload)
            local_mqtt.publish('hermes/tts/sayFinished', msg.payload)
        else:
            print 'Could not publish : {}'.format(msg.topic)


local_mqtt.on_connect = on_connect
local_mqtt.on_disconnect = on_disconnect
local_mqtt.on_message = on_message
local_mqtt.connect(config.get('global').get('mqtt-host'), int(config.get('global').get('mqtt-port')))
local_mqtt.loop_forever()

