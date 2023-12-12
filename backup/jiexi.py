from os import path
import sys
import requests


def jiexi(link):
    url = "https://www.yuanxiapi.cn/api/jiexi_video/"

    rsp = requests.get(url=url, headers=headers, params={"url": link})

    return rsp.json()


def download(d_url, file_name):
    print(file_name+".mp4", "下载中。。。")
    with open(path.join(path.dirname(__file__), file_name + ".mp4"), "wb") as f:
        rsp = requests.get(d_url, headers=headers)
        f.write(rsp.content)
    print(file_name+".mp4", "下载完成！")


if __name__ == "__main__":
    
    global headers
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    if len(sys.argv) == 1:
        link = input("请输入链接：")
        rsp = jiexi(link)
        file_name = link.split("/")[-1]
        print(rsp["video"])
        download(rsp["video"], file_name)
    else:
        args = sys.argv[1:]
        with open(args[0], 'r') as f:
            lines = f.readlines()

        links = [line.rstrip() for line in lines]
        file_name = 0
        for link in lines:
            rsp = jiexi(link)
            if rsp["code"] != 200:
                print(f"此链接未解析成功：{link}")
                continue
            file_name += 1
            print(rsp)
            download(rsp["video"], str(file_name))


