import json
import os
import time
import random
import paho.mqtt.client as mqtt

client = mqtt.Client(os.environ['DEV_ID'])
client.tls_set()
client.tls_insecure_set(True)

client.username_pw_set('use-token-auth', os.environ['MQTT_TOKEN'])
client.connect(os.environ['MQTT_HOST'], 8883, 60)

n = random.randint(20,80)
ts = time.strftime('%s')
payload = {'d':{ts: n}}
client.publish('iot-2/evt/test/fmt/json', json.dumps(payload),1)
client.loop()
client.disconnect()
