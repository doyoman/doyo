import re
import requests
from bs4 import BeautifulSoup
import os
import telegram

"""
为了适配青龙识别定时：
cron "30 7 * * *" script-path=https://github.com/doyoman/doyo/raw/main/teacher.py, tag=教师招聘信息爬虫
new Env('教师招聘信息爬虫')
"""

provinces = ["hn","gd"]
TOKEN = os.getenv("EU_BOT")
ID = os.getenv("EU_ID")
bot = telegram.Bot(token=TOKEN)

for province in provinces:
    if province == "hn":
        citys = ["zz", "cs"]
    elif province == "gd":
        citys = ["gz",]

    for city in citys:
        url = "http://" + province + ".zgjsks.com/html/jiaozhao/ksgg/" + city

        headers={
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
        }

        rep = requests.get(url=url,headers=headers)
        rep.encoding='gbk'
        html = rep.text
        bs = BeautifulSoup(html,'html.parser')
        text = bs.find_all("div",class_="c_list")
        find = re.compile(r'.*</a><a href="(.*)" target="_blank" title=".*">(.*)</a></span><i>(.*)</i></li>')
        gonggao_list = re.findall(find,str(text))
        messages = []
        for item in gonggao_list[0:6]:
            message = "\n".join(item)
            messages.append(message)
        bot.send_message(chat_id=ID,text="\n----------\n".join(messages))
        if city == "zz":
            print("株洲信息发送完成！")
        elif city == "cs":
            print("长沙信息发送完成！")
        elif city == "gz":
            print("广州信息发送完成！")


# print(text)
