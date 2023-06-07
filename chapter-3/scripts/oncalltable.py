import json
import datetime
import os
import sys

if not sys.argv[1]:
    print("No emails provided, exiting")
    sys.exit()
emails = sys.argv[1]
emailList = emails.split(",")

oncallEmail=emailList[0]
escalationEmail=emailList[1]

data={"InResponseOncall":[]}
base = datetime.datetime.today()
date_list = [i.strftime("%d/%m/%Y") for i in [base + datetime.timedelta(days=x) for x in range(-1,7)] ]

for j in date_list:
    item={  "PutRequest": { "Item": {   "TeamId": { "S":"devops"},"Day": { "S":j} , "oncall":{"S":oncallEmail},"escalation":{"S" :escalationEmail}    }   }}
    data['InResponseOncall'].append(item)

cdir = os.path.dirname(__file__)
file = os.path.join(cdir, '../data/oncalltable.json')
f=open(file,"w")
f.write(json.dumps(data,indent=4))
f.close()


