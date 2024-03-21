import random
import time
import json
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client

broker = '192.168.28.118'
port = 1883
topic_publish = "kondisi/status"
client_id = 'python-mqtt'
username = ''
password = ''

GPIO.setmode(GPIO.BOARD)

led = 31
ldr = 33
id_device = 'al3'

GPIO.setup(led, GPIO.OUT)
GPIO.setup(ldr, GPIO.IN)

GPIO.output(led, False)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        
        if rc == 0:
            print("Has successfully connected !")
        else:
            print("Failed to connect")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publishSubscribe(client):
    
    msg_count = 0

    while True:
        
        GPIO.output(led, False)
        print(GPIO.input(ldr))    
        
        if GPIO.input(ldr) == False:
            status = 'Lampu menyala'
            kondisi = 'Gelap'
            GPIO.output(led, False)
            msg = json.dumps({"id_device":id_device, "kondisi":kondisi, "status":status, "value":GPIO.input(ldr)})
            result = client.publish(topic_publish, msg)
            time.sleep(1)
            
        else:
            status = 'Lampu tidak menyala'
            kondisi = 'Terang'
            GPIO.output(led, True)
            msg = json.dumps({"id_device":id_device, "kondisi":kondisi, "status":status, "value":GPIO.input(ldr)})
            result = client.publish(topic_publish, msg)
            time.sleep(1)

        status = result[0]

        if status == 0:
            print("Send "+msg+" to topic "+topic_publish)
        else:
            print("Failed to send message to {topic_publish}")
        time.sleep(1)

def run():
    client = connect_mqtt()
    client.loop_start()
    publishSubscribe(client)
    
if _name_ == '_main_':
    run()