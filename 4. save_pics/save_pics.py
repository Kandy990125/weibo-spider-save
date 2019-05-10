# -*- coding: UTF-8 -*-
import requests
import os
import pathlib
import json
class Downloader:
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}

    def open_file(self):
        with open("final2.json","rb") as f:
            s = f.read()
            self.dir = json.loads(s)
            i = 0
            for item in self.dir:
                uname = item["uname"]
                print("site_name:",uname)
                infos = item["info"]
                for info in infos:
                    text = info["text"]
                    if "#林彦俊[超话]#" not in text:
                        continue
                    time = info["time"]
                    for pic in info["pics"]:
                        try:
                            self.save_main(time, uname, pic)
                            print("第" + str(i) + "张照片下载完毕")
                            i = i + 1
                        except:
                            print("照片下载失败，失败id：",pic)

    def save_main(self,created_time,uname,picid):
        if pathlib.Path("D:\\pics\\"+ created_time).exists() == False:
            os.makedirs("D:\\pics\\"+ created_time)
        if pathlib.Path("D:\\pics\\" + created_time+"\\"+uname).exists() == False:
            os.makedirs("D:\\pics\\" + created_time+"\\"+uname)
        url = "https://wx1.sinaimg.cn/large/"+picid+".jpg"
        response = requests.get(url, headers=self.headers)
        img = response.content
        with open("D:\\pics\\" + created_time+"\\"+uname+"\\"+picid+".jpg",'ab' ) as f:
            f.write(img)

down = Downloader()
down.open_file()