# Simple function to call the Google Translate API and return the translated language

from flask import current_app, request
import json
import requests
import pprint
# Google Translation REST API URL. Docs at
# https://cloud.google.com/translate/docs/translating-text#translate-translate-text-protocol
translationApiUrl = "https://translation.googleapis.com/language/translate/v2"

apiKey = ""
with open("/secrets/default/google-api-key/key") as f:
    apiKey = f.read()

def translate(text, fromLang, toLang):
    req = { "q": text, "source": fromLang, "target": toLang, "key": apiKey }
    resp = requests.get(translationApiUrl, params = req)
    if resp.status_code != 200:
        return ("Error %s: %s" % (resp.status_code, resp.text)), resp.status_code
    result = resp.json()
    return result

def main():
    log_request(request)
    try:
        text = request.json["text"]           #.get("text", "Hello, world!")
        fromLang = request.json["from"] or "" #.get("from", "")
        toLang = request.json["to"] or "en"   #.get("to", "en")
        
        current_app.logger.info("Translating %s from %s to %s" % (text, fromLang, toLang))

        translationResponse = translate(text, fromLang, toLang)

        return "%s\n" % translationResponse["data"]["translations"][0]["translatedText"]
    except Exception as e:
        current_app.logger.error("error %s" % e)
        return "Error", 500


def log_request(req):
    request_dict = {
        "url": req.url,
        #"args": req.args,
        "content_type": req.content_type,
        "authorization": req.authorization,
        #"cache_control": req.cache_control,
        "content_length": req.content_length,
        "content_encoding": req.content_encoding,
        "cookies": req.cookies,
        "form": req.form,
        "data": req.get_data()
    }
    s = pprint.pformat(request_dict)
    current_app.logger.info("Request:\n---\n%s\n---" % s)

