import os

from dotenv import load_dotenv

from coinchart import Livecoinwatch
from linemessage import app, send_notify


def send_to_line_notify():
    load_dotenv()
    line_nofiry_token = os.environ.get('NTFYTKN')
    token = os.environ.get('TOKEN')
    Livecoinwatch(token, crypto=['____GST', 'SOL']).run(mode='to_image')
    send_notify(line_nofiry_token, '即時 GST / SOL 匯率報告：', filepath='exchange_rate.png')


if __name__ == '__main__':
    # send_to_line_notify()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
