import re
import os
import requests

bot_token = os.getenv('TG_BOT_TOKEN')
chat_id = os.getenv('TG_USER_ID')

def get_zlm():
    log_name = os.popen('ls /ql/log/code/*.log').read().replace('\n', '')
    f = open(log_name,'r',encoding='utf-8').read() #/ql/log/code/*.log

    Name_List = ['Fruit', 'Pet', 'Bean', 'DreamFactory', 'JdFactory', 'Jxnc', 'Cash', 'Sgmh', 'Health']
    texts = []
    for name in Name_List:
        ex = "My{}[0-9]*=\'(.*?)\'".format(name)
        zlm ='&'.join(re.findall(ex, f))
        if name == 'Fruit':
            text = '<b>东东农场助力码：</b>\n/farm ' + zlm
        elif name == 'Pet':
            text = '<b>东东萌宠助力码：</b>\n/pet ' + zlm
        elif name == 'Bean':
            text = '<b>种豆得豆助力码：</b>\n/bean ' + zlm
        elif name == 'DreamFactory':
            text = '<b>京喜工厂助力码：</b>\n/jxfactory ' + zlm
        elif name == 'JdFactory':
            text = '<b>东东工厂助力码：</b>\n/ddfactory ' + zlm
        elif name == 'Jxnc':
            text = '<b>京喜农场助力码：</b>\n' + zlm
        elif name == 'Cash':
            text = '<b>签到领现金助力码：</b>\n' + zlm
        elif name == 'Sgmh':
            text = '<b>闪购盲盒助力码：</b>\n/sgmh ' + zlm
        elif name == 'Health':
            text = '<b>京东健康助力码：</b>\n/health ' + zlm
        else:
            text = name + '没有发现助力码！'
        texts.append(text)
    send_message('\n\n'.join(texts))

def send_message(text):
    # telegram推送
    bot_data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    url = "https://api.telegram.org/bot" + bot_token + "/sendMessage"
    requests.post(url=url, data=bot_data)

if __name__ == '__main__':
    get_zlm()