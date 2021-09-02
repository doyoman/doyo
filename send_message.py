import requests
import os

chat_id = os.getenv("EU_ID")
bot_token = os.getenv("EU_BOT")

def send_message(text):
    #telegram推送
    bot_data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'html'
    }
    url = "https://api.telegram.org/bot" + bot_token + "/sendMessage"
    rep = requests.post(url=url, data=bot_data)
    if rep.status_code != 200:
        print('telegram 推送失败')
    else:
        print('telegram 推送成功')
