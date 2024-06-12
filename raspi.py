from Crypto.Cipher import AES
from paho.mqtt import client as mqtt_client
import random
import time,json,base64
from gpiozero import MotionSensor

broker = 'broker.emqx.io'
port = 1883
topic = "motion_detection_topic"

key = b'\xe6\xc7\xa7\xda\xda$\x820G\x02\xc4\xad\x1c3\x9e\xce'

def encrypt(msg):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('utf-8'))
    return nonce, ciphertext, tag

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect to MQTT Broker!")

    client = mqtt_client.Client(f"publisher-{random.randint(0, 1000)}")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    pir = MotionSensor(14, sample_rate=1)  

    while True:
        time.sleep(1)

        if pir.motion_detected:
            data = "Motion not detected"
        else:
            data = "Motion  detected"

        nonce, ciphertext, tag = encrypt(data)
        msg = {
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "tag": base64.b64encode(tag).decode('utf-8')
        }
        result = client.publish(topic, json.dumps(msg))
        status = result[0]
        if status == 0:
            print(f"Published '{data}' to topic '{topic}'")
        else:
            print(f"Failed to publish message to topic '{topic}'")
import base64

def publish(client):
    pir = MotionSensor(14, sample_rate=1)  

    while True:
        time.sleep(1)

        if pir.motion_detected:
            data = "Motion detected"
        else:
            data = "Motion not detected"

        nonce, ciphertext, tag = encrypt(data)
        msg = {
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "tag": base64.b64encode(tag).decode('utf-8')
        }
        result = client.publish(topic, json.dumps(msg))
        status = result[0]
        if status == 0:
            print(f"Published '{data}' to topic '{topic}'")
        else:
            print(f"Failed to publish message to topic '{topic}'")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if _name_ == '_main_':
    run()