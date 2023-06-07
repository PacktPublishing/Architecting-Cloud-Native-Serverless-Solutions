# Setup Instructions

## What you need

- One AWS account with administrative access
- Three email addresses
  - One for sending the alerts
  - Two for receiving the alerts - one each for the oncall engineer and manager
- Git and AWS CLI - AWS CLI should be setup with the right IAM credentials
- Python3 and boto3 library installed
- An IDE of choice if you wish to modify the code
- jq JSON parser CLI for parsing AWS CLI outputs

## Outline of the process to setup and test the project

- Use the provided script to update AWS SES to add three email identities
- Run the AWS CloudFormation template to provision the cloud resources using aws CLI.  This include
  - Four DynamoDB Tables
    - Config: Storing configuration - current incident id for auto-increment
    - Incident: All incidents
    - Service - Storing Service to Team ownership relation
    - Oncall - Oncall calendar for teams
  - Two Lambda Functions and its IAM Role and Policy
    - IncidentProcessor - Accept the incident from API Gateway, process it, store to Incdient table and initiate step function
    - IncidentNotifier - Invoked by the step function for sending email to oncall and escalation
  - One Step Function and its IAM Role and Policy
    - Used to send email alert to oncall engineer and alert the manager after 5 minutes
  - One HTTP API Gateway V2 and IAM policy
    - One Endpoint for all action
    - PUT method to store incident
    - POST method to modify incident - only for claiming incident
    - GET method to retrieve incident
    - No authentication
  - Three Parameter Store Entries
    - Sender Email for SES
    - State machine ARN for Lambda IncientProcessor
    - API Endpoint - for creators to retrieve the base URL
- Update the code for two lambda functions - processor and notifier
  - Each function a single python file with handler and other methods
  - These file are in its own diretories and should be archived to a zip file
  - Once the zip file is created, they can be uploaded and applied to the lambda functions using aws CLI
- Insert test data to the dynamodb tables
  - Incident Table doesnt require any data
  - Config Table and Service Table
    - Load the dummy data from the json file provided
  - Oncall table
    - Use the provided script to generate oncall data for one week 
  - Use aws CLI to batch load the data to the tables


## Setup Instructions

Checkout this repo and change to the root directory of the repo. Then switch to the 'chapter-3' directory 

```
git clone git@github.com:PacktPublishing/Architecting-Cloud-Native-Serverless-Solutions.git
cd chapter-3
```

The repo is structured as follows:

```
.
|-- cloudformation
|   `-- inresponse.cf.yml
|-- data
|   |-- dynamo-data.json
|   |-- invalid-incident.json
|   |-- oncalltable.json
|   `-- sample-incident.json
|-- lambda
|   |-- notifier
|   |   `-- lambda_function.py
|   `-- processor
|       `-- lambda_function.py
|-- scripts
|   |-- oncalltable.py
|   `-- ses-email-verify.py
`-- README.md
```
Let us go through each steps

### Add three email addresses to SES

- AWS Simple Email Service need to verify each email before using it to send out messages
- For this you need to add these emails ( called identities in SES) to SES for verification
- SES email addition is not supported by cloudformation, hence a utility script is provided to add the three emails to SES
- Once these emails are added for verification each will receive a verification link from AWS
- Each email need to be manually verified post whcih they can be used for sending and receiving emails

- We need three email ids for this experiment, one for sending email, two for receiving - oncall and escalation.
- For demonstrations, we are using three fictional emails - alerts@inresponse.com,oncall@inresponse.com,escalation@inresponse.com
- When running these automations, please replace the emails with real ones

To verify these identities, run the following command

```
python3 scripts/ses-email-verify.py alerts@inresponse.com,oncall@inresponse.com,escalation@inresponse.com
```

If all goes good, you will see one request ID per email as output.
Failing of this script is not a blocker for deploying the solution, but when you run it the email sending will fail

## Run the cloudfromation template to create all AWS resources

This template will create all resource required and then save the API endpoint to AWS parameter store, which can be used for testing out the alerting sevice .  Replace the email `alerts@inresponse.com` with the right sender email

```
aws cloudformation create-stack --stack-name inresponse-v01 --template-body file://./cloudformation/inresponse.cf.yml --parameters ParameterKey=SenderEmail,ParameterValue=alerts@inresponse.com --capabilities CAPABILITY_NAMED_IAM
```

This will return a stack id which can be used for checking the status. The following command should return `CREATE_COMPLETE`

```
aws cloudformation describe-stacks --stack-name inresponse-v01|jq ".Stacks[0].StackStatus"
```

Once the stack creeation is completed you can retrieve the API endpoint from parameter store and save it in a shell variable to be used later

```
ALERTS_API_ENDPOINT=$(aws ssm get-parameter --name /inresponse/apiendpoint|jq -r ".Parameter.Value")
```

The value would be something like `https://abcd12345.execute-api.ap-south-1.amazonaws.com` with the first and third part of the domain name varying

## Update the code for both lambda functions

The lambda functions were created with dummy code, now we need to update the function code as follows.

```
cd lambda

zip -r processor.zip processor

zip -r notifier.zip notifier

aws lambda update-function-code --function-name InResponseIncidentProcessor1 --zip-file fileb://processor.zip

aws lambda update-function-code --function-name InResponseIncidentNotifier --zip-file fileb://notifier.zip

cd ..
```

## Insert data into DynamoDB tables

First let us generate oncall data.  Thee is a sample file that contains dummy data in the data directory, following script will overwrite it.  Provide the oncall and escalation emails as comma seperated list to the script

```
python3 scripts/oncalltable.py oncall@inresponse.com,escalation@inresponse.com
```

Now load this and the `dynamo-data.json` file to DDB

```
aws dynamodb batch-write-item --request-items file://./data/dynamo-data.json

aws dynamodb batch-write-item --request-items file://./data/oncalltable.json

```

This completes our setup, now we can test the API

## API Testing

First let us submit a valid incident to the API

```
curl -s ${ALERTS_API_ENDPOINT} -H "content-type: application/json" -X PUT -d @data/sample-incident.json

{"message": "Added incident with incident number 1001"}

```

Repeat this command a few time so that your DB will have some more incidents.

Now let us try an invlid incident ( this is the same incident as before , with the service name changed to a name that is not in the Service DDB table )

```
curl -s ${ALERTS_API_ENDPOINT} -H "content-type: application/json" -X PUT -d @data/invalid-incident.json
{"message": "Invalid Service"}
```
Now let us retrieve the incident we created

```
curl -s ${ALERTS_API_ENDPOINT}/1002 -H "content-type: application/json" -X GET|jq .
{
  "service": "athena",
  "IncidentId": "1002",
  "source": "nagios",
  "time": "1639171486",
  "description": "5xx error rate above 5% in payment service",
  "severity": "ERR",
  "state": "OPEN",
  "title": "5xx Error Spike"
}
```
Try to retrieve a non-existing incident

```
curl -s ${ALERTS_API_ENDPOINT}/1022 -H "content-type: application/json" -X GET
{"message": "Incident Not found"}
```

By now the first email alert will be received at oncall@inresponse.com and after five minutes the escalation email will be received at escalation@inresponse.com

Now let us try to acknowledge the incident to prevent escalation.  Try this within five minutes of the incident is created - to verify incident is not escalated and you dont receive any emails to escalation@inresponse.com

```
curl -s ${ALERTS_API_ENDPOINT}/1002 -H "content-type: application/json" -X POST -d '{"state":"CLAIMED"}' | jq .
{
  "message": "Changed instance state to CLAIMED"
}
```

Let us try to modify something else

```
 curl -s ${ALERTS_API_ENDPOINT}/1002 -H "content-type: application/json" -X POST -d '{"service":"mysql"}' |jq .
{
  "message": "Only supported update is incident state"
}
```

This completes the testing and covers all the features provided by the alerting system.  Delete the cloudformation stack to avoid additional cost from AWS

```
aws cloudformation delete-stack --stack-name inresponse-v01

aws cloudformation describe-stacks --stack-name inresponse-v01|jq ".Stacks[0].StackStatus"
"DELETE_IN_PROGRESS"
```




