import os
import re
import requests
import json

'''
cron: */15 * * * *
'''

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
env_name = 'LOCAL_ADD6'

def get_add6():
    output = os.popen('ifconfig').read()
    add6 = re.findall(r'inet6 addr: (.*?) Scope:Global', output)[0].split('/')[0]
    return add6

def search_env_name(token):
    url = 'http://localhost:5700/open/envs?searchValue={}'.format(env_name)
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json;charset=UTF-8'
    }
    rsp = requests.get(url=url, headers=headers).json()
    return rsp

def get_token():
    url = 'http://192.168.2.100:5700/open/auth/token?client_id={}&client_secret={}'.format(client_id, client_secret)
    res = requests.get(url)
    token = res.json()['data']['token']
    return token

def put_add6(token, add6, eid):
    url = 'http://localhost:5700/open/envs'
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json;charset=UTF-8'
    }
    data = {"name": env_name, "value": add6, "_id": eid}
    data = json.dumps(data)
    rsp = requests.put(url=url, headers=headers, data=data)

def insert_add6(token, add6):
    url = 'http://localhost:5700/open/envs'
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json;charset=UTF-8'
    }
    data = [{"name": env_name, "value": add6}]
    data = json.dumps(data)
    rsp = requests.post(url=url, headers=headers, data=data)

if __name__=='__main__':
    add6 = get_add6()
    token = get_token()
    rsp = search_env_name(token)
    if len(rsp['data']) == 0:
        print('未找到所设环境变量！开始自动添加。')
        print('本地最新IPV6地址为：' + add6)
        insert_add6(token, add6)
        print('添加完成！')
    else:
        print('找到所设环境变量！')
        old_add6 = rsp['data'][0]['value']
        print('本地最新IPV6地址为：' + add6)
        print('环境变量中存储的IPV6地址为：' + old_add6)
        if add6 == old_add6:
            print('IPV6地址未改变，无需更新。')
        else:
            print('IPV6地址已改变，开始更新。')
            eid = rsp['data'][0]['_id']
            put_add6(token, add6, eid)
            print('更新完成！')
