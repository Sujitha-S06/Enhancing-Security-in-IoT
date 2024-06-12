import paho.mqtt.client as mqtt
from Crypto.Cipher import AES
import json
import base64


key = b'\xe6\xc7\xa7\xda\xda$\x820G\x02\xc4\xad\x1c3\x9e\xce'
def decrypt(nonce, ciphertext, tag):
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        return plaintext.decode('utf-8')
    except:
        return False


def on_message(client, userdata, message):
    
    data = json.loads(message.payload.decode())

    
    nonce = base64.b64decode(data["nonce"])
    ciphertext = base64.b64decode(data["ciphertext"])
    tag = base64.b64decode(data["tag"])

    
    plaintext = decrypt(nonce, ciphertext, tag)

    
    if plaintext:
        print("Decrypted message:", plaintext)
    else:
        print("Failed to decrypt message")


broker = 'broker.emqx.io'
port = 1883


client = mqtt.Client()

client.connect(broker, port)
print("Connected to MQTT broker")


client.on_message = on_message


topic = "motion_detection_topic"
client.subscribe(topic)
print(f"Subscribed to topic '{topic}'")


client.loop_forever()