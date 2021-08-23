from requests import session
import requests
import random
import os

"""
为了适配青龙识别定时：
cron "5 7 * * *" script-path=https://github.com/doyoman/doyo/raw/main/checkin.py, tag=几鸡签到
new Env('几鸡签到')
"""

########################
bot_token = os.getenv("EU_BOT")
chat_id = os.getenv("EU_ID")
username = os.getenv("EU_USERNAME")
password = os.getenv("EU_PASSWORD")
########################

def checkin():
    sess = session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    login_url = "https://a.luxury/signin?c=" + str(random.random())

    data = {
        "email":username,
        "passwd":password
    }
    #登录
    sess.post(url=login_url, headers=headers, data=data)
    #签到
    checkin_url = "https://j05.space/user/checkin?c=" + str(random.random())
    checkin_response = sess.post(url=checkin_url,headers=headers).json()['msg']

    print(checkin_response)
    send_messages("<b>几鸡签到:</b>\n" + checkin_response)

def send_messages(text):
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

if __name__ == '__main__':
    checkin()
