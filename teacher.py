import re
import requests
from bs4 import BeautifulSoup
import os

provinces = ["hn","gd"]
TOKEN = os.getenv("Teacher_Token")
ID = os.getenv("EU_ID")

def send_messages(text):
    #telegram推送
    bot_data = {
                'chat_id': ID,
                'text': text,
                'parse_mode': 'Markdown'
    }
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    rep = requests.post(url=url, data=bot_data)
    if rep.status_code != 200:
        print('telegram 推送失败')
        print(rep.text)
    else:
        print('telegram 推送成功')

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
        text = "\n----------\n".join(messages)
        send_messages(text)
        if city == "zz":
            print("株洲信息发送完成！")
        elif city == "cs":
            print("长沙信息发送完成！")
        elif city == "gz":
            print("广州信息发送完成！")
