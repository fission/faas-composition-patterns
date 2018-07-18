from flask import request, current_app
import json
import requests
import time

VISION_FUNCTION_URL = "http://router.fission/vision"
TRANSLATION_FUNCTION_URL = "http://router.fission/translation"

def main():
    # Image to process
    imgUrl = request.json["url"]

    # Language to translate to
    targetLang = "en"
    if "lang" in request.json:
        targetLang = request.json["lang"]

    #
    # Call vision function over HTTP.
    #
    t1 = time.time()
    resp = requests.post(VISION_FUNCTION_URL, json = { "url": imgUrl })

    if resp.status_code != 200:
        # Just give up on error, though we could potentially retry
        # depending on the type of error.
        return ("Error identifying text %s: %s" % (resp.status_code, resp.text)), resp.status_code

    text = resp.text

    #
    # Call transation function over HTTP.
    #
    t2 = time.time()
    resp = requests.post(TRANSLATION_FUNCTION_URL, json = { "text": text, "to": targetLang, "from": "en" })

    if resp.status_code != 200:
        return ("Error translating %s: %s" % (resp.status_code, resp.text)), resp.status_code

    translated_text = resp.text

    t3 = time.time()

    # Log the time spent in each request.
    current_app.logger.info("Vision function took %s sec, translation function took %s sec" % (t2 - t1, t3 - t2))
    
    return translated_text, 200
