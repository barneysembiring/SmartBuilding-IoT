import random
import time
import json
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client

broker = '192.168.28.118'
port =  1883
topic_publish = "topic/flame"
topic_subscribe = "topic/fsensor"
client_id = 'python-mqtt'
username =''
password =''

led = 7
buzz = 4
flame = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(buzz, GPIO.OUT)
GPIO.setup(flame, GPIO.IN)

def callback(flame):
    print("flame detected")

GPIO.add_event_detect(flame, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(flame, callback)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username,password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publishSubscribe(client):
    msg_count = 0
    while True:
        print(GPIO.input(flame))
        if GPIO.input(flame) == 1:
            GPIO.output(buzz, False)
            GPIO.output(led, True)
            msg = json.dumps({"buzz": "OFF","led": "ON", "status":"Tidak Terdeteksi", "value": GPIO.input(flame)})
            result = client.publish(topic_publish, msg)
            time.sleep(1)
        else:
            GPIO.output(buzz, True)
            GPIO.output(led, False)
            msg = json.dumps({"buzz": "ON","led": "OFF", "status":"Terdeteksi", "value": GPIO.input(flame)})
            result = client.publish(topic_publish, msg)
            time.sleep(1)

    status = result[0]
    if status == 0:
        print("Send "+msg+" to topic {topic_publish}")
    else:
        print("Failed to send message to topic {topic_publish}")
    
    def on_message(client, userdata, msg):
        print("Received "+str(msg.payload)+" from topic")
    client.on_message = on_message
    time.sleep(1)
    
def run():
    client = connect_mqtt()
    client.loop_start()
    publishSubscribe(client)

if _name_ == '_main_':
    run()