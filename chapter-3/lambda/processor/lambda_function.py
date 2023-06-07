import json
import time
import boto3
from re import split as rsplit

responseTemplate={
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": json.dumps({'message': 'Dummy message'})
}

def lambda_handler(event,context):
    if event['requestContext']['http']['method'] == 'GET':
        incidentId=rsplit("[\/?]", event['requestContext']['http']['path'] )[1]
        response = getmethod(incidentId)
    elif event['requestContext']['http']['method'] == 'POST':
        incident=json.loads( event['body'] )
        incidentId=rsplit("[\/?]", event['requestContext']['http']['path'] )[1]
        response = postmethod(incident,incidentId)
    elif event['requestContext']['http']['method'] == 'PUT':
        incident=json.loads( event['body'] )
        response = putmethod(incident)
    return response
    

def getmethod(incidentId):
    dynamodb =  boto3.resource('dynamodb')
    incidentTable = dynamodb.Table("InResponseIncident")
    try:
        incidentData =  incidentTable.get_item(
        Key={
            'IncidentId': incidentId
         }
        )
        responseTemplate['statusCode'] = 200
        responseTemplate['body'] = json.dumps(incidentData['Item'])
        return responseTemplate
    except Exception as e:
        responseTemplate['statusCode'] = 404
        responseTemplate['body'] = json.dumps({"message":"Incident Not found"})
        return responseTemplate

def putmethod(request):
    dynamodb =  boto3.resource('dynamodb')
    ## Insert to incident Table
    incident = request
    # Check for minimum required keys in the incident
    if not all(k in incident for k in ("service","severity","description","title") ):
        responseTemplate['statusCode'] = 400
        responseTemplate['body'] = json.dumps({ "message": "Invalid incident format"})        
        return responseTemplate
    serviceTable = dynamodb.Table('InResponseService')
    serviceData = serviceTable.get_item(
        Key={
            'ServiceId': incident['service']
        }
    )
    if "Item" not in serviceData:
        responseTemplate['statusCode'] = 400
        responseTemplate['body'] = json.dumps({ "message": "Invalid Service"})
        return responseTemplate
    incident['IncidentId'] = str(getIncUUID())
    incident['state'] = "OPEN"
    incident['time'] = str(int(time.time()))
    incidentTable = dynamodb.Table("InResponseIncident")
    try:
       responseTemplate['statusCode'] = 200
       incidentTable.put_item(Item=incident)
       ssm = boto3.client('ssm')
       param = ssm.get_parameter(Name='/inresponse/statemachinearn')
       stateMachineArn=param['Parameter']['Value']
       client = boto3.client('stepfunctions')
       client.start_execution(
         stateMachineArn=stateMachineArn,
         input=json.dumps(incident)
         )
       responseTemplate['body'] = json.dumps({ "message": "Added incident with incident number " + str( incident['IncidentId'] )})
       return responseTemplate
    except Exception as e:
        responseTemplate['statusCode'] = 500
        responseTemplate['body'] = json.dumps({ "message": "Unable to insert/alert incident " + str( incident['IncidentId'] )})
        return responseTemplate    
    

def postmethod(request,incidentId):
    if  list(request.keys()) != ['state']:
        responseTemplate['statusCode'] = 400
        responseTemplate['body'] = json.dumps({ "message": "Only supported update is incident state"})
        return responseTemplate
    dynamodb =  boto3.resource('dynamodb')
    incidentTable = dynamodb.Table("InResponseIncident")
    try:
        incidentTable.update_item(
            Key={
                'IncidentId': incidentId
             },
        UpdateExpression='SET #ste = :val1',
        ExpressionAttributeValues={
            ':val1': request['state']
        },
          ExpressionAttributeNames={
        "#ste": "state"
        }
        )
        responseTemplate['body'] = json.dumps({ "message": "Changed instance state to " + request['state'] })
        return responseTemplate
    except Exception as e:
        responseTemplate['body'] = json.dumps({ "message": "Failed to update state" })
        responseTemplate['statusCode'] = 500
        return responseTemplate
    

def getIncUUID():
    dynamodb = boto3.resource('dynamodb')
    configTable = dynamodb.Table('InResponseConfig')
    ddbResponse = configTable.update_item(
                Key={
                        "ConfigKey": "IncidentId"
        },
     UpdateExpression='ADD CurrentId :increment',
     ExpressionAttributeValues={
                                ':increment': 1
        },
     ReturnValues="UPDATED_NEW"
    )
    return(ddbResponse['Attributes']['CurrentId'])
