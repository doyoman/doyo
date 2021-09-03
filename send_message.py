import requests
import os

#用于仓库内脚本发送通知

########获取环境变量##########

CHAT_ID = os.getenv("EU_ID")
BOT_TOKEN = os.getenv("EU_BOT")
BARK_KEY = os.getenv("BARK_PUSH")

##############################

def send_message(title,text):
    print(text,"\n")
    if len(BOT_TOKEN) != 0:    #telegram推送
        bot_data = {
            'chat_id': CHAT_ID,
            'text': text,
            'parse_mode': 'html'
        }
        url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
        rep = requests.post(url=url, data=bot_data)
        if rep.status_code != 200:
            print('telegram 推送失败')
        else:
            print('telegram 推送成功')
    if len(BARK_KEY) != 0:    #bark推送
        rep = requests.post('https://api.day.app/' + BARK_KEY + "/" + text)
        if rep.status_code != 200:
            print('Bark 推送失败')
        else:
            print('Bark 推送成功')

