import os

import requests
from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import ImageSendMessage, MessageEvent, TextMessage, TextSendMessage

from coinchart import Livecoinwatch
from introduction import intro_text

app = Flask(__name__)
load_dotenv()
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))
url = os.environ.get('URL')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    load_dotenv()
    token = os.environ.get('TOKEN')
    url = os.environ.get('URL')
    if event.message.text == 'GST 換算 SOL':
        Livecoinwatch(token, crypto=['____GST', 'SOL']).run(mode='to_image')
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/exchange_rate.png',
                preview_image_url=f'{url}/static/exchange_rate.png',
            ),
        )
    elif event.message.text == 'SOL 月價格':
        Livecoinwatch(token, crypto=['SOL']).get_coin_chart(mode='to_coin_image')
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/SOL.png',
                preview_image_url=f'{url}/static/SOL.png',
            ),
        )
    elif event.message.text == 'SOL 週價格':
        Livecoinwatch(token, crypto=['SOL'], period=7).get_coin_chart(
            mode='to_coin_image'
        )
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/SOL.png',
                preview_image_url=f'{url}/static/SOL.png',
            ),
        )
    elif event.message.text == 'SOL 日價格':
        Livecoinwatch(token, crypto=['SOL'], period=1).get_coin_chart(
            mode='to_coin_image'
        )
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/SOL.png',
                preview_image_url=f'{url}/static/SOL.png',
            ),
        )
    elif event.message.text == 'GST 月價格':
        Livecoinwatch(token, crypto=['____GST']).get_coin_chart(mode='to_coin_image')
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/____GST.png',
                preview_image_url=f'{url}/static/____GST.png',
            ),
        )
    elif event.message.text == 'GST 週價格':
        Livecoinwatch(token, crypto=['____GST'], period=7).get_coin_chart(
            mode='to_coin_image'
        )
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/____GST.png',
                preview_image_url=f'{url}/static/____GST.png',
            ),
        )
    elif event.message.text == 'GST 日價格':
        Livecoinwatch(token, crypto=['____GST'], period=1).get_coin_chart(
            mode='to_coin_image'
        )
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/____GST.png',
                preview_image_url=f'{url}/static/____GST.png',
            ),
        )
    elif event.message.text == 'GMT 月價格':
        Livecoinwatch(token, crypto=['____GMT']).get_coin_chart(mode='to_coin_image')
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/____GMT.png',
                preview_image_url=f'{url}/static/____GMT.png',
            ),
        )
    elif event.message.text == 'GMT 週價格':
        Livecoinwatch(token, crypto=['____GMT'], period=7).get_coin_chart(
            mode='to_coin_image'
        )
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/____GMT.png',
                preview_image_url=f'{url}/static/____GMT.png',
            ),
        )
    elif event.message.text == 'GMT 日價格':
        Livecoinwatch(token, crypto=['____GMT'], period=1).get_coin_chart(
            mode='to_coin_image'
        )
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=f'{url}/static/____GMT.png',
                preview_image_url=f'{url}/static/____GMT.png',
            ),
        )
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=intro_text))


def send_notify(token, msg, filepath=None, stickerPackageId=None, stickerId=None):
    payload = {'message': msg}
    headers = {"Authorization": "Bearer " + token}
    if stickerPackageId and stickerId:
        payload['stickerPackageId'] = stickerPackageId
        payload['stickerId'] = stickerId

    if filepath:
        attachment = {'imageFile': open(filepath, 'rb')}
        print(attachment)
        r = requests.post(
            "https://notify-api.line.me/api/notify",
            headers=headers,
            params=payload,
            files=attachment,
        )
    else:
        print("attachment")
        r = requests.post(
            "https://notify-api.line.me/api/notify", headers=headers, params=payload
        )
    return r.status_code, r.text
