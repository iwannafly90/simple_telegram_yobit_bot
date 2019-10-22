import json

from flask import Flask
from flask import request
from flask import jsonify
import requests


app = Flask(__name__)

try:
    import settings
except ImportError:
    print("File settings.py not found. Copy file settings.py.default and rename in to the settings.py. "
          "Don't forget to set token variable")

MAIN_URL = settings.MAIN_URL


def get_price_in_usd(coin):
    """
    Getting price of the user coin, converted to usd, using Yobit public api

    :param coin: coin, that was written by user
    :return: str
    """
    url = f'https://yobit.net/api/2/{coin.lower()}_usd/ticker'
    response = requests.get(url).json()
    if not 'error' in response:
        price = response['ticker']['last']
        return str(price) + ' usd'
    else:
        return 'Указана неверная валюта. Валюту нужно указывать так, как она называется на сайте Yobit. ' \
               'Например, btc, eth, ltc'


def send_message(chat_id, text='Wait a second, please'):
    """
    Sending the message to the chat

    :param chat_id: id of the chat, that will get the message
    :param text: text of the message, that will send to the chat
    :return: None
    """
    send_message_url = MAIN_URL + f'sendmessage?chat_id={chat_id}&text={text}'
    requests.get(send_message_url)


@app.route('/', methods=['POST', 'GET'])
def get_request():
    """
    Getting request from telegram. It's using webhooks.

    You should use setWebhook method of api to get the requests from telegram, otherwise bot wouldn't work

    Example:
    https://api.telegram.org/bot<token>/setWebhook?url=URL_Of_Your_site
    """

    if request.method == 'POST':
        response = request.get_json()
        chat_id = response['message']['chat']['id']
        message = response['message']['text']

        send_message(chat_id, get_price_in_usd(message))
        return jsonify(response)
    return ''


if __name__ == '__main__':
    app.run()

