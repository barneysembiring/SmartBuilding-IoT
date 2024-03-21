import RPi.GPIO as GPIO
import time
import json
import random
from paho.mqtt import client as mqtt_client

broker = '192.168.43.208'
port = 1883
topic_publish = "topic/flame"
topic_subscribe = "topic/kebakaran"
client_id = 'python-mqtt'
username = ''
password = ''

buzzer = 7
flame = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(flame, GPIO.IN)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publishSubscribe(client):
    msg_count = 0
    while True:
        i = GPIO.input(flame)
        GPIO.output(buzzer, False)
        if i == False:
            GPIO.output(buzzer, True)
            msg = json.dumps({"status":"Api terdeteksi", "value": GPIO.input(flame)})
            result = client.publish(topic_publish, msg)
            time.sleep(1)
        else:
            GPIO.output(buzzer, False)
            msg = json.dumps({"status":"Api tidak terdeteksi", "value": GPIO.input(flame)})
            result = client.publish(topic_publish, msg)
            time.sleep(1)

    status = result[0]
    if status == 0:
        print("Send"+msg+"to topic {topic_publish}")
    else:
        print("Failed to send message to topic {topic_publish}")

    def on_message(client, userdata, msg):
        print("Received"+str(msg.payload)+"from topic")
        client.on_message = on_message
        time.sleep(1)
def run():
    client = connect_mqtt()
    client.loop_start()
    publishSubscribe(client)

if _name_ == '_main_':
