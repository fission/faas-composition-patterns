
from flask import current_app, request
import json
import requests

# Google Vision API URL. Docs at https://cloud.google.com/vision/docs/request
visionApiUrl = "https://vision.googleapis.com/v1/images:annotate"

# Google Translation REST API URL. Docs at
# https://cloud.google.com/translate/docs/translating-text#translate-translate-text-protocol
translationApiUrl = "https://translation.googleapis.com/language/translate/v2"

apiKey = ""
with open("/secrets/default/google-api-key/key") as f:
    apiKey = f.read()

# Create a Google Vision API request
def requestForImageURL(url):
    return 

#
# Vision: Get text from picture of text
#
def vision(imgUrl):
    try:
        requestUrl = visionApiUrl + ("?key=%s" % apiKey)
        visionReq = { "requests": [ { "image": { "source": { "imageUri": imgUrl } },
                             "features": [ { "type": "TEXT_DETECTION" } ] } ] }
        resp = requests.post(requestUrl, json = visionReq)
        if resp.status_code != 200:
            return ("Error %s: %s" % (resp.status_code, resp.text)), resp.status_code
        result = resp.json()
        current_app.logger.info("Response = %s" % result)
        return result
    except Exception as e:
        current_app.logger.error("error %s" % e)
        return "Error", 500

#
# Translate languages
#
def translate(text, fromLang, toLang):
    req = { "q": text, "source": fromLang, "target": toLang, "key": apiKey }
    resp = requests.get(translationApiUrl, params = req)
    if resp.status_code != 200:
        return ("Error %s: %s" % (resp.status_code, resp.text)), resp.status_code
    result = resp.json()
    return result


#
# Get image URL, call vision, call translation, return translated text.
#
def main():
    imgUrl = request.form["url"]
    visionResponse = vision(imgUrl)
    text = visionResponse["responses"][0]["textAnnotations"][0]["description"]
    translationResponse = translate(text, "", "en")
    translatedText = translationResponse["data"]["translations"][0]["translatedText"]
    return translatedText + "\n", 200
    
