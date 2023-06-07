# Pseudo IoT device with MQTT client

Now that we have setup the Watson IoT platform as descibed in the [previous section](WatsonIoT.md), we need to take the next step to create a client to send messages to this platform.  As you would remember, we had created an IoT device in the paltform.  This device is a representation of an actual IoT device that can communicate with the platform using MQTT protocol.  But given that most of our readers may not have an IoT device readily avilable, we will use a python script to send MQTT message to this platform.  So in this implementation a python script would emulate the device we added in the Watson platform.

## Connecting to the Watson Platform

Details instruction for this is given in the ibm cloud documentation [here](https://cloud.ibm.com/docs/IoT/reference/security/connect_devices_apps_gw.html)

This is the summary of what we need.  

_orgid: The organiztaion id of you the Watson IoT instance you created earlier.  This was `35v16x`

_devicetype: Type of the device that was added to the platform - for us this was temperature-sensor

_deviceid: ID of the device that was added - this is temp-sensor-101 in our case

We had also created a security token in the previous section: `y&c*yMm!Tw34`

Now that we have these parameters, we can connect to the MQTT broker of our IoT platform.  The MQTT host is your org id preppended to messaging.internetofthings.ibmcloud.com.  Device ID is a combination of org id, device type and device id.
We will create a shell script called `env.sh` to export the required connection parameters as environement variables as given below

```
export MQTT_HOST=35v16x.messaging.internetofthings.ibmcloud.com
export MQTT_PORT=8883
export DEV_ID=d:35v16x:temperature-sensor:temp-sensor-101
export MQTT_USER=use-token-auth
export MQTT_TOKEN='y&c*yMm!Tw34'
```

Run the following command to export all these variables into the shell that is going to run the python script we are about to create.

```
source env.sh
```

Now that we have the necessary parameters, we can use a python script to send messages to this endpoint.  We will be using the Paho MQTT python package for this.  Install it as given below.

```
pip3 install paho-mqtt
```

You can find the script below.  This script can be run in regular intervals to send messages to the paltform.

*this code can also be found in the following file [code/pseudo-iot.py](code/pseudo-iot.py)*

https://github.com/PacktPublishing/Architecting-Cloud-Native-Serverless-Solutions/blob/7d09edc44adc5cbc32a6bd7152f6518b39035c1b/chapter-8/code/pseudo-iot.py#L1-L19

Now you can run this code as 
```
python3 code/pseudo-iot.py
```

You can also run it every 30 seconds in a loop like this:
```
while true;do python3 code/pseudo-iot.py;done
```
