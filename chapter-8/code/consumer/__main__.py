import os
import sys
import time
import json
import paho.mqtt.client as mqtt
from ibmcloudant.cloudant_v1 import CloudantV1, Document

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):  
    print("Connected with result code {0}".format(str(rc)))  
    # Subscribe to the topic 
    msg = client.subscribe(userdata['MQTT_TOPIC'],1)  
    print(msg)

# Callback for when a message published to the topic is received
def on_message(client, userdata, msg):  
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    mqmsg = json.loads(msg.payload.decode("utf-8"))
    client = CloudantV1.new_instance(service_name="CLOUDANT")
    doc = Document.from_dict(mqmsg)
    rr=client.post_document(db='serverless-db1',document=doc)
    print(rr.result['id'])

# Callback function for subscription
def on_subscribe(client, userdata, mid, granted_qos): 
    print("Subscribed")

def main(params):
    os.environ['CLOUDANT_URL']=params['CLOUDANT_URL']
    os.environ['CLOUDANT_APIKEY']=params['CLOUDANT_APIKEY']
    client = mqtt.Client(params['DEVICE_ID'],False,params)  # Create client instance for this application/cloud function”
    # Enabled secure communication with TLS
    client.tls_set()
    client.tls_insecure_set(True)
    # Set auth parameters
    client.username_pw_set(params['API_KEY'],params['AUTH_TOKEN'])
    # Set callback function for successful connection
    client.on_connect = on_connect
    # Set callback function for receipt of a message
    client.on_message = on_message
    # Set call back for succesfull subscription
    client.on_subscribe = on_subscribe
    # Connect to the MQTT Broker
    client.connect(params['MQTT_HOST'], int(params['MQTT_PORT']), 60)

    # Run a loop for 15 seconds to pull all published messages and then exit.
    # We are using this instead of a long running process as the 
    # cloud funtion will be running on scheduled interval of one minute
    
    startTime = time.time()
    runTime = 15
    while True:
        client.loop()
        currentTime = time.time()
        if (currentTime - startTime) > runTime:
            break

    client.disconnect()
    return({"status": "Complete"})

if __name__ == '__main__':
    params=json.load(open(sys.argv[1]))
    main(params)
