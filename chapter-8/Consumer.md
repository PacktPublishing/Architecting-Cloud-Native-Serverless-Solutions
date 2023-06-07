# Consumer cloud function / openwhisk action creation

We need a cloud function that can read from the MQTT broker (as the topic consumer) and write down each record into Cloudant DB for persistence.

The code is available at the following location:

[code/consumer/](code/consumer/)

Inorder to connect to IoT platform as a consumer, you need to create an application in the IoT platform.  To do this, from the IoT platform dashbaord go to `Apps > API Keys.` This page will hve an option to generate API Keys.  Follow the onscreen instructions, When asked for the "Role", select "Standard Application".  When finished, you will get an API Key and authentication token.  Note them down safely as it wont be shown again.

The device ID for the consumer should have the format "a:org_id:subscriber_name"

org_id is the org id of your IoT platform and substriber name can be whatever you chose.

You will also need the Cloudant credentials you save in the earlier step.  This will include a cloudant URL and cloudant api key.

Inorder to create the function, first checkout this repository to a directory and switch to that directory.  

```
cd chapter-8/code/consumer
```

Modify the `consumer_fn.json` file and replace the values for API_KEY,AUTH_TOKEN,DEVICE_ID using the information from Watson.  Also modify the CLOUDANT_URL and CLOUDANT_APIKEY from the credentials you save earlier.

Then follow the below steps:

```
python3 -m venv virtualenv
source virtualenv/bin/activate
pip3 install -r requirements.txt
deactivate
 cp activate_this.py virtualenv/bin/
zip -r consumer.zip __main__.py virtualenv
 ibmcloud fn action create consumer consumer.zip --kind python:3.9 --param-file consumer_fn.json
```
This would create the cloud function.  If you have already send MQTT messages to the platform using the [code/pseudo-iot.py](code/pseudo-iot.py) script, then you can invoke this function and see if it is adding the message to Cloudant.

```
$ ibmcloud fn action invoke consumer -r
{
    "status": "Complete"
}
$ ibmcloud fn activation list |grep -m 1 consumer
2022-07-16 17:18:49 dd3f7ec77fb44b97bf7ec77fb4fb975f python:3.9 cold  18.291s    success         safeercm@g...com_dev/consumer:0.0.5
$ ibmcloud fn activation get dd3f7ec77fb44b97bf7ec77fb4fb975f|sed '1d'|jq .logs
[
  "2022-07-16T17:19:07.934001Z    stdout: Connected with result code 0",
  "2022-07-16T17:19:07.934068Z    stdout: (0, 1)",
  "2022-07-16T17:19:07.934146Z    stdout: Message received-> iot-2/type/temperature-sensor/id/temp-sensor-101/evt/test/fmt/json b'{\"temp\": 44, \"timestamp\": 1657991918, \"device\": \"d:35v16x:temperature-sensor:temp-sensor-101\"}'",
  "2022-07-16T17:19:07.934146Z    stdout: 95a50d49514acdd8a8f5f758056fbb15",
  "2022-07-16T17:19:07.934146Z    stdout: Subscribed"
]
```
As you can see, it is able to subscribe and retrieve messages from MQTT broker and push to Cloudant DB.  Next we can create the function to process the cloudant event notification and alert base on that.  The documentation can be found [here](Alerting.md)
