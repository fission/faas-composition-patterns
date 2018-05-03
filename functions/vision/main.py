# Simple function to call the Google Vision API.  Does OCR and label
# detection, and return the first label if there's no text.

from flask import current_app, request
import json
import requests

# Google Vision API URL. Docs at https://cloud.google.com/vision/docs/request
visionApiUrl = "https://vision.googleapis.com/v1/images:annotate"

apiKey = ""
with open("/secrets/default/google-api-key/key") as f:
    apiKey = f.read()

# Create a Google Vision API request
def requestForImageURL(url):
    return { "requests": [ { "image": { "source": { "imageUri": url } },
                             "features": [ { "type": "TEXT_DETECTION" },
                                           { "type": "LABEL_DETECTION" } ] } ] }

def vision(imgUrl):
    try:
        requestUrl = visionApiUrl + ("?key=%s" % apiKey)
        visionReq = requestForImageURL(imgUrl)
        resp = requests.post(requestUrl, json = visionReq)
        if resp.status_code != 200:
            return ("Error %s: %s" % (resp.status_code, resp.text)), resp.status_code
        result = resp.json()
        current_app.logger.info("Response = %s" % result)
        return result
    except Exception as e:
        current_app.logger.error("error %s" % e)
        return "Error", 500

def main():
    imgUrl = request.form["url"]
    visionResponse = vision(imgUrl)

    # If it's a picture of text, return that text. Otherwise, return a
    # description of what we see.
    text = ""
    r = visionResponse["responses"][0]
    current_app.logger.info("r = %s", r)
    if "textAnnotations" in r:
        text = r["textAnnotations"][0]["description"]
    elif "labelAnnotations" in r:
        text = r["labelAnnotations"][0]["description"]

    return "%s\n" % text, 200

