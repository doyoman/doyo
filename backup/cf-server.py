#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import csv
import base64
import json
from random import choice
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def Converter():
    if request.args.get("sub") is None:
        return "链接格式不正确，请在url后衔接订阅链接，如/?sub=http://xxxxxx"
    return main(request.args.get("sub"))


@app.route("/cf_ip", methods=["POST"])
def Receive_ip():
    if request.files.get("result.csv") is None:
        return "未上传!"

    request.files.get("result.csv").save("result.csv")
    return "ok"    


def main(sub_url):
    def get_sub(url):
        rsp = requests.get(url)
        b_list = base64.b64decode(rsp.text)
        list = str(b_list, "utf-8").strip().split("\n")
        # print(list)
        return list

    def re_vmess(vmess):
        dic = json.loads(str(base64.b64decode(vmess[8:]), "utf-8"))
        # print(dic["add"])
        dic["add"] = choice(ip_list)
        # print(dic)
        return "vmess://" + str(base64.b64encode(json.dumps(dic, ensure_ascii=False).encode()), "utf-8")

    def get_cf_ip():
        ip_list = []
        with open(r'result.csv', encoding='utf-8')as f:
            reader = csv.reader(f)
            headers = next(reader)
            # print(headers)
            for row in reader:
                ip_list.append(row[0])
                # print(row[0])
        return ip_list

    sub = get_sub(sub_url)
    ip_list = get_cf_ip()
    new_sub_list = []
    for vmess in sub:
        new_vmess = re_vmess(vmess)
        new_sub_list.append(new_vmess)

    new_sub = str(base64.b64encode(
        str("\n".join(new_sub_list)).encode()), "utf-8")
    # print(new_sub)
    return new_sub


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2087)
