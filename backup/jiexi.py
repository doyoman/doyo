# from os import path
import sys
import you_get
import requests


def jiexi(link):
    url = "https://www.yuanxiapi.cn/api/video/"

    rsp = requests.get(url=url, headers=headers, params={"url": link})

    return rsp.json()


def download(d_url, file_name):
    sys.argv = ["you-get", "-O", file_name, d_url]
    you_get.main()
    # print(file_name+".mp4", "下载中。。。")
    # with open(path.join(path.dirname(__file__), file_name + ".mp4"), "wb") as f:
    #     rsp = requests.get(d_url, headers=headers)
    #     f.write(rsp.content)
    # print(file_name+".mp4", "下载完成！")


if __name__ == "__main__":
    link = input("请输入链接：")
    #link = sys.argv[1]
    global headers
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    rsp = jiexi(link)
    file_name = rsp["url"].split("/")[-1]
    if file_name =="":
        file_name = rsp["url"].split("/")[-2]
    print(rsp["video"])
    download(rsp["video"], file_name)
