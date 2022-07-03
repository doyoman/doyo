import os
import requests
import time
from send_message import send_message

'''
cron: 30 0-23/6 * * *
'''

headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
        }
list_url = "https://raw.githubusercontent.com/doyoman/doyo/main/backup/list.json"

try:
    list = requests.get(list_url, headers).json()
except:
    list = requests.get("https://ghproxy.com/" + list_url, headers).json()

text_list = []

for app in list:
    app_id = app["id"]
    app_country = app["country"]
    app_name = app["name"]
    url = "https://itunes.apple.com/lookup?id={}&country={}".format(app_id, app_country)
    price = requests.get(url=url, headers=headers).json()['results'][0]['price']
    if app_country == "cn":
        symbol = "¥"
    elif app_country == "us":
        symbol = "$"
    else:
        print("此国家金额标识未添加！")
    text = "{}   ==>   {}{}".format(app_name, price, symbol)
    text_list.append(text)

times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
message = "AppStore价格监控:\n\n" + "\n".join(text_list) + "\n\n数据更新于 " + times
send_message(message)
