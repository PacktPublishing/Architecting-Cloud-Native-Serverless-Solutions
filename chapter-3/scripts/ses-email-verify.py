import boto3
import sys
import re

if not sys.argv[1]:
    print("No emails provided, exiting")
    sys.exit()
emails = sys.argv[1]
emailList = emails.split(",")
emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
ses = boto3.client('ses')
for email in emailList:
    if not re.fullmatch(emailRegex,email):
        print("Identity ",email," is not in email format")
        continue
    try:
        response = ses.verify_email_identity(
        EmailAddress = email 
        )
        print(response['ResponseMetadata']['RequestId'])
    except Exception as e:
        print("Failed to add email identity - " ,  email , " - for verification")
        print(str(e))
