import requests
import time
from notify import send

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
    url = f"https://itunes.apple.com/lookup?id={app_id}&country={app_country}"
    try:
        rsp = requests.get(url=url, headers=headers).json()
        price = rsp['results'][0]['formattedPrice']
        text = f"{app_name}   ==>   {price}"
    except:
        text = f"{app_name}   ==>   查询失败！"
    text_list.append(text)

times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
message = "\n".join(text_list) + "\n\n数据更新于 " + times
print(message)
send("AppStore价格监控:", message)
