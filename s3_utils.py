import boto3

import requests

from io import BytesIO
import boto3

import requests

from io import BytesIO
import json

bucket_url = "http://ssiaeration-images.s3-website-us-west-2.amazonaws.com/"

def add_image(im, im_uuid):
    # Saves an image to s3 bucket under the name <im_uuid>.json
    if im.mode != "RGB":
        im = im.convert("RGB")

    img_io = BytesIO()
    im.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)

    s3 = boto3.resource('s3')
    s3.Bucket('ssiaeration-images').put_object(Key=im_uuid+".jpg", Body=img_io, ACL='public-read')

    img_link = bucket_url + im_uuid + ".jpg"
    return img_link

def add_prediction(prediction, im_uuid):
    # JSON-ise a prediction and saves it to s3 bucket under the name <im_uuid>.json
    s3 = boto3.resource('s3')

    prediction_io = BytesIO()
    json.dump(prediction, prediction_io)

    prediction_io.seek(0)
    s3.Bucket('ssiaeration-images').put_object(Key=im_uuid+".json", Body=prediction_io, ACL='public-read')

def load_prediction(im_uuid):
    # Returns a tuple: the json.content as well as a python version of the json.
    link = bucket_url + im_uuid + ".json"

    # Raw json
    json_file = requests.get(link)
    # Python list version
    prediction = json.load(BytesIO(json_file.content))

    return json_file.content, prediction
