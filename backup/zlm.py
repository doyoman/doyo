import re
import os
import requests

bot_token = os.getenv('TG_BOT_TOKEN')
chat_id = os.getenv('TG_USER_ID')

def get_zlm():
    log_name = os.popen('ls /ql/log/code/*.log').read().replace('\n', '')
    f = open(log_name,'r',encoding='utf-8').read()

    Name_List = ['Fruit', 'Pet', 'Bean', 'DreamFactory', 'JdFactory', 'Sgmh', 'Health'] #  , 'Jxmc'
    for name in Name_List:
        ex = "My{}[0-9]*=\'(.*?)\'".format(name)
        zlm ='&'.join(re.findall(ex, f))
        if name == 'Fruit':
            text = '/farm ' + zlm #  <b>东东农场助力码：</b>\n
        elif name == 'Pet':
            text = '/pet ' + zlm #  <b>东东萌宠助力码：</b>\n
        elif name == 'Bean':
            text = '/bean ' + zlm #  <b>种豆得豆助力码：</b>\n
        elif name == 'DreamFactory':
            text = '/jxfactory ' + zlm #  <b>京喜工厂助力码：</b>\n
        elif name == 'JdFactory':
            text = '/ddfactory ' + zlm #  <b>东东工厂助力码：</b>\n
        elif name == 'Sgmh':
            text = '/sgmh ' + zlm #  <b>闪购盲盒助力码：</b>\n
        elif name == 'Health':
            text = '/health ' + zlm #  <b>京东健康助力码：</b>\n
        # elif name == 'Jxmc':
        #     jxmc_log = os.popen('ls -r /ql/log/JDHelloWorld_jd_scripts_jd_jxmc | sed -n "1p"').read().replace('\n', '')
        #     jxmc = open('/ql/log/JDHelloWorld_jd_scripts_jd_jxmc/' + str(jxmc_log), encoding='utf-8').read()
        #     text = '/jxmc ' + '&'.join(re.findall('助力码： (.*)', jxmc))
        else:
            text = name + '没有发现助力码！'
        send_message(text)

def send_message(text):
    # telegram推送
    bot_data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    url = "https://api.telegram.org/bot" + str(bot_token) + "/sendMessage"
    requests.post(url=url, data=bot_data)

if __name__ == '__main__':
    get_zlm()