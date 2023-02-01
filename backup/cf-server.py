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

    if request.args.get("me"):
        return main(request.args.get("sub"), me=True)
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

def main(sub_url, me=False):
    def get_sub(url):
        rsp = requests.get(url)
        b_list = base64.b64decode(rsp.text)
        list = str(b_list, "utf-8").strip().split("\n")
        # print(list)
        return list

    def re_vmess(vmess):
        SW = []
        if LT_list:
            dic1 = json.loads(str(base64.b64decode(vmess[8:]), "utf-8"))
            dic1["add"] = choice(LT_list)
            dic1["ps"] = dic1["ps"] + "-联通优选"
            
            SW.append("vmess://" + str(base64.b64encode(json.dumps(dic1, ensure_ascii=False).encode()), "utf-8"))
        
        if DX_list:
            dic2 = json.loads(str(base64.b64decode(vmess[8:]), "utf-8"))
            dic2["add"] = choice(DX_list)
            dic2["ps"] = dic2["ps"] + "-电信优选"
            SW.append("vmess://" + str(base64.b64encode(json.dumps(dic2, ensure_ascii=False).encode()), "utf-8"))
        
        if YD_list:
            dic3 = json.loads(str(base64.b64decode(vmess[8:]), "utf-8"))
            dic3["add"] = choice(YD_list)
            dic3["ps"] = dic3["ps"] + "-移动优选"
            SW.append("vmess://" + str(base64.b64encode(json.dumps(dic3, ensure_ascii=False).encode()), "utf-8"))
        
        return SW

    def get_GY_ip():
        url = "https://api.hostmonit.com/get_optimization_ip"
        payload = "{\"key\":\"iDetkOys\"}"
        headers = {
        'Content-Type': 'text/plain'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()

    def get_cf_ip():
        LT_list = []
        DX_list = []
        YD_list = []

        if not me:
            rsp = get_GY_ip()
            for i in rsp["info"]:
                if i["line"] == "CM":
                    YD_list.append(i["ip"])
                elif i["line"] == "CU":
                    LT_list.append(i["ip"])
                elif i["line"] == "CT":
                    DX_list.append(i["ip"])
            return LT_list,DX_list,YD_list

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
