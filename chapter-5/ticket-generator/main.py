from google.cloud.spanner_dbapi.connection import connect
from google.cloud import storage

import functions_framework
import json
import base64
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

@functions_framework.cloud_event
def numplate_handler(cloud_event):
  data = json.loads(base64.b64decode(cloud_event.data['message']['data']).decode('utf-8'))
  print(data)
  bucket_name=data['bucket']
  blob_name=data['blob']
  plate=data['plate']

  local_blob="blob_local"
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(blob_name)
  blob.download_to_filename(local_blob)

  instance_id = os.environ.get('DBINSTANCE')
  database_id = os.environ.get('DBNAME')
  table = os.environ.get('TABLE')

  connection = connect(instance_id, database_id)
  connection.autocommit = True

  cursor = connection.cursor()
  cursor.execute("SELECT * FROM " + table + " where NumPlate='" + plate + "'" )

  result = cursor.fetchone()
  print(result)
  cursor.close()

  ticket_file = plate + ".pdf"
  c = canvas.Canvas( ticket_file , pagesize=A4)
  w, h = A4
  text = c.beginText(50, h - 50)
  text.setFont("Times-Roman", 12)
  c.setTitle("Traffic Overspeed Notice")
  text.textLines("\n\n                    Traffic Overspeed Notice")
  c.drawText(text)
  c.line(50, h - 60,500,h - 60)
  text = c.beginText(50, h - 80)
  text.textLines("Dear " + result[1] + ",\n\n     Your vehicle number " + plate + " is found to be overspeeding and your are hereby directed \n to pay a fine of INR 1000\n\n")
  c.drawText(text)
  c.drawImage( local_blob, 50, h - 500, width=350, height=350)
  c.save()

  bucket = storage_client.get_bucket( os.environ.get('TICKET_BUCKET') )
  blob = bucket.blob(ticket_file)
  blob.upload_from_filename(ticket_file)

