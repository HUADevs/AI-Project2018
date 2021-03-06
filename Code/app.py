import os
import sys
from datetime import datetime

import requests
from flask import Flask, request, json

from bot import Bot

VERIFY_TOKEN = "test_token"
PAGE_ACCESS_TOKEN = "EAAaVttkZBpccBAHYsxd7jZAr1l1oIGHxxobFXZBrnZBFwvQfpZCBnog5TeiZBZBADdZB1lwXI1wZC7K1LnDXDTxHvAYTZC3bxP9XTZBZCf2K59kZCGZCBZBYY1GTb4T1EcHpy8JTfZAlnyxaRrwtVIDBZCyEBrL4PNmRZCaqo9gVxDUaVuFGA48AZDZD"
bot = Bot(name='Jarvis', facebook_input=True)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"][
                        "id"]  # the recipient's ID, which should be your page's facebook ID
                    if 'text' in messaging_event['message']:
                        message_text = messaging_event["message"]["text"]  # the message's text
                    else:
                        message_text = 'sticker'
                    bot.decide_action(facebook_input=message_text)
                    for fb_response in bot.facebook_response:
                        send_message(sender_id, fb_response)
                        # bot.facebook_response.remove(fb_response)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = str(msg).format(*args, **kwargs)
        print(u"{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
