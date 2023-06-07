import os
import json
from flask import Flask, request
from google.cloud import storage
from google.cloud import pubsub_v1

import sys
import cv2
import numpy as np
import imutils
import pytesseract

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.json
    bucket_name  = data['bucket']
    blob_name = data['name']
    print(f"Detected change in Cloud Storage bucket: {bucket_name} object {blob_name}" )
    local_blob="blob_local"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(local_blob)
    num_plate = anpr(local_blob)
    topic_path=os.environ.get("TOPIC_PATH")
    pubmsg(topic_path,num_plate,bucket_name,blob_name)
    return (f"Detected change in Cloud Storage bucket: {bucket_name} object {blob_name}.  Plate returned {num_plate}", 200)

def pubmsg(topic_path, plate,bucket,blob):
    publisher = pubsub_v1.PublisherClient()
    message = {
        "plate": plate,
        "bucket": bucket,
        "blob": blob
    }
    data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f'published message with id {future.result()}')


def anpr(imageFile):
    image_original = cv2.imread(imageFile)
    image_grayscale = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)

    image_bfilter = cv2.bilateralFilter(image_grayscale, 13, 15, 15)
    image_edges = cv2.Canny(image_bfilter, 30, 200)

    image_contours = cv2.findContours(image_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(image_contours)
    contours_topten = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    nameplate_polygon = None
    for contour in contours_topten:
        polygon = cv2.approxPolyDP(contour, 10, True)
        if len(polygon) == 4:
            nameplate_polygon = polygon
            break

    mask = np.zeros(image_grayscale.shape, np.uint8)
    nameplate_border = cv2.drawContours(mask, [nameplate_polygon], 0,255, -1)
    nameplate_masked = cv2.bitwise_and(image_original, image_original, mask=mask)

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = image_grayscale[x1:x2+1, y1:y2+1]

    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    text = pytesseract.image_to_string(cropped_image,config='--psm 7 --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', lang='eng')
    text=text.strip().replace(" ", "")
    print(text)
    return text


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
