import RPi.GPIO as GPIO
import time
import json
import random
from paho.mqtt import client as mqtt_client

broker = '192.168.28.118'
port = 1883
topic_publish = "topic/pir"
topic_subscribe = "topik/pintu"
client_id = 'python-mqtt'
username = ''
password = ''

pinInfra = 16
relay = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinInfra, GPIO.IN)
GPIO.setup(relay, GPIO.OUT)

def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Terhubung ke mqtt broker")
            else:
                print("gagal terhubung, ulang program %d\n", rc)
        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

def publishSubscribe(client):
    msg_count = 0
    while True:
        GPIO.output(relay, False)
        if GPIO.input(pinInfra):
            GPIO.output(relay, False)
            msg = json.dumps({"status":"Ada gerakan", "value": GPIO.input(pinInfra)})
            result = client.publish(topic_publish, msg)
            while GPIO.input(pinInfra):
                time.sleep(5)
        else:
            GPIO.output(relay, True)
            msg = json.dumps({"status":"Tidak ada gerakan", "value": GPIO.input(pinInfra)})
            result = client.publish(topic_publish, msg)
            time.sleep(1)
    
    status = result[0]
    if status == 0:
        print("Send"+msg+"to topic {topic_publish}")
    else:
        print("Failed to send massage to topic {topic_publish}")
        
    def on_message (client, userdata, msg):
        print("Reseived"+str(msg.payload)+"from topic")
        client.on_message = on_message
        time.sleep(1)
def run():
    client = connect_mqtt()
    client.loop_start()
    publishSubscribe(client)
    
if _name_ == '_main_':
    run()