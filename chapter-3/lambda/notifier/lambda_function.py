import json
import os
import boto3
from datetime import date

def lambda_handler(event, context):
    # TODO implement
    response={
        'statusCode': 200,
        'body': json.dumps('Alerting may not have worked')
    }
    incident=event['incident']
    escalationType=event['escalationType']
    dynamodb =  boto3.resource('dynamodb')
    if escalationType == 'escalation':
        incidentTable = dynamodb.Table("InResponseIncident")
        try:
            incidentData =  incidentTable.get_item(
            Key={
                'IncidentId': incident['IncidentId']
             }
            )
        except Exception as e:
            print("No such incident")
        if incidentData['Item']['state'] != 'OPEN':
            response['statusCode'] = 400
            response['body']= json.dumps("Incident " + str(incident['IncidentId']) +" is not open, cant escalate")
            return response
    serviceTable = dynamodb.Table("InResponseService")
    service=incident['service']
    serviceData = serviceTable.get_item(
        Key={
            'ServiceId': service
        }
    )
    team = serviceData['Item']['TeamId']
    oncallTable=dynamodb.Table("InResponseOncall")
    today=date.today().strftime("%d/%m/%Y")
    oncallData=oncallTable.get_item(
        Key={
            'TeamId': team,
            'Day': today
        }
        )
    escalationEmail=oncallData['Item'][escalationType]
    sendEmail(escalationEmail,incident,escalationType)
    return response
    

def sendEmail(endpoint,incident,escalationType):
    from botocore.exceptions import ClientError

    ssm = boto3.client('ssm')
    param = ssm.get_parameter(Name='/inresponse/senderemailv1')
    SENDER=param['Parameter']['Value']
    RECIPIENT = endpoint
    AWS_REGION = "ap-south-1"
    SUBJECT = incident['severity'] + ": " + str(incident['IncidentId']) + ": " + incident['title']
    if escalationType == 'escalation':
        SUBJECT = 'Escalation! ' + SUBJECT
    BODY_TEXT = incident['description']
    BODY_HTML = incident['description']
    CHARSET = "UTF-8"

    client = boto3.client('ses',region_name=AWS_REGION)

    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
