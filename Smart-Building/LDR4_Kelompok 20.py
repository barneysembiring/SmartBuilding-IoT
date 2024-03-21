import RPi.GPIO as GPIO
import random
import time
import json
from paho.mqtt import client as mqtt_client

broker = '192.168.28.118'
port = 1883
topic_publish = "topic/Kesya"
topic_subscribe = "topic/Otomatis"
client_id = 'python-mqtt'
username = ''
password = ''
GPIO.setwarnings(False)

#GPIO pin set up
pinLdr = 11
pinLed = 3
IN1 = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinLdr, GPIO.IN)
GPIO.setup(pinLed, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)

GPIO.output(pinLed, False)
GPIO.output(IN1, False)

#ID_DEVICE
id_device = 'd4'
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
        GPIO.output(pinLed, 0)
        GPIO.output(IN1, False)
        print(GPIO.input(pinLdr))
        if GPIO.input(pinLdr)==0:
            status = 'Lampu mati'
            GPIO.output(IN1, False)
            msg = json.dumps({"id": id_device, "value":GPIO.input(pinLdr), "status":status})
            result = client.publish(topic_publish, msg)
            GPIO.output(pinLed, 0)	#Matikan LED
            time.sleep(1)
        else:
            status = 'Lampu hidup'
            GPIO.output(IN1, True)
            msg = json.dumps({"id": id_device, "value":GPIO.input(pinLdr), "status":status})
            result = client.publish(topic_publish, msg)
            GPIO.output(pinLed, 1)	#Hidupkan LED
            time.sleep(1)
        status = result[0]
        if status == 0:
            print("Send"+msg+"to topic {topic_publish}")
        else:
            print("Failed to send message to topic {topic_publish}")
        def on_message(client, userdata, msg):
            print("Received"+str(msg.payload)+"from topic")
        client.subscribe(topic_subscribe)
        client.on_message = on_message
        time.sleep(1)
def run():
    client = connect_mqtt()
    client.loop_start()
    publishSubscribe(client)
if __name__ == '__main__':
    run()