#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import csv
import base64
import json
import os
from random import choice
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def Converter():
    if request.args.get("sub") is None:
        return "链接格式不正确，请在url后衔接订阅链接，如/?sub=http://xxxxxx"
    return main(request.args.get("sub"))


@app.route("/LT_ip", methods=["POST"])
def Receive_LT():
    if request.files.get("result.csv") is None:
        return "未上传!"

    request.files.get("result.csv").save("LT.csv")
    return "ok"    

@app.route("/DX_ip", methods=["POST"])
def Receive_DX():
    if request.files.get("result.csv") is None:
        return "未上传!"

    request.files.get("result.csv").save("DX.csv")
    return "ok"

@app.route("/YD_ip", methods=["POST"])
def Receive_YS():
    if request.files.get("result.csv") is None:
        return "未上传!"

    request.files.get("result.csv").save("YD.csv")
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
        SW = []
        if LT_list:
            dic["add"] = choice(LT_list)
            dic["ps"] = dic["ps"] + "-联通优选"
            SW.append("vmess://" + str(base64.b64encode(json.dumps(dic, ensure_ascii=False).encode()), "utf-8"))
        
        if DX_list:
            dic["add"] = choice(DX_list)
            dic["ps"] = dic["ps"] + "-电信优选"
            SW.append("vmess://" + str(base64.b64encode(json.dumps(dic, ensure_ascii=False).encode()), "utf-8"))
        
        if YD_list:
            dic["add"] = choice(YD_list)
            dic["ps"] = dic["ps"] + "-移动优选"
            SW.append("vmess://" + str(base64.b64encode(json.dumps(dic, ensure_ascii=False).encode()), "utf-8"))
        
        return SW

    def get_cf_ip():
        LT_list = []
        DX_list = []
        YD_list = []
        if os.path.exists("./LT.csv"):
            with open(r'LT.csv', encoding='utf-8')as f:
                reader = csv.reader(f)
                headers = next(reader)
                # print(headers)
                for row in reader:
                    LT_list.append(row[0])
                    # print(row[0])
        
        if os.path.exists("./DX.csv"):
            with open(r'DX.csv', encoding='utf-8')as f:
                reader = csv.reader(f)
                headers = next(reader)
                # print(headers)
                for row in reader:
                    DX_list.append(row[0])
                    # print(row[0])
        
        if os.path.exists("./YD.csv"):
            with open(r'YD.csv', encoding='utf-8')as f:
                reader = csv.reader(f)
                headers = next(reader)
                # print(headers)
                for row in reader:
                    YD_list.append(row[0])
                    # print(row[0])

        return LT_list,DX_list,YD_list

    sub = get_sub(sub_url)
    LT_list,DX_list,YD_list = get_cf_ip()
    new_sub_list = []
    for vmess in sub:
        new_vmessS = re_vmess(vmess)
        for i in new_vmessS:
            new_sub_list.append(i)

    new_sub = str(base64.b64encode(
        str("\n".join(new_sub_list)).encode()), "utf-8")
    # print(new_sub)
    return new_sub


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2087)
