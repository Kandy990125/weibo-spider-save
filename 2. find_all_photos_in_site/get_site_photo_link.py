# -*- coding: UTF-8 -*-
import requests
import json
import time
headers = {
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
def get_site_photo_link(id,name):
    usr_info = {}
    usr_info["uid"] = id
    usr_info["uname"] = name
    usr_info_list = []
    for i in range(1,100):
        url = "https://m.weibo.cn/api/container/getIndex?type=uid&value="+id+"&containerid=107603"+id+"&page=" + str(i)
        print(url)
        rep = requests.get(url,headers=headers)
        rep_dir = json.loads(rep.text)
        if rep_dir["ok"] == 0:
            break
        cards = rep_dir["data"]["cards"]
        for item in cards:
            try:
                i = item["mblog"]
            except:
                continue
            dir = {}
            dir["id"] = item["mblog"]["id"]
            dir["text"] = item["mblog"]["text"]
            dir["time"] = item["mblog"]["created_at"]
            try:
                pic_list = item["mblog"]["pics"]
            except:
                # print(dir["id"])
                continue
            pics = []
            for picinfo in pic_list:
                picid = picinfo["pid"]
                pics.append(picid)
            dir["pics"] = pics
            usr_info_list.append(dir)
        time.sleep(3)
    usr_info["info"] = usr_info_list
    return usr_info

def get_id_name():
    with open("site_name.json", "rb") as f:
        text = f.read()
        list = json.loads(text)
        for item in list:
            name = item["name"]
            print(name)
            url = item["url"]
            id = str(url).split('/')[4]
            dir = get_site_photo_link(id,name)
            text = json.dumps(dir,ensure_ascii=False)
            print(name,text)
            with open("site_info_new.json","a+") as f2:
                f2.write(json.dumps(text)+"\n")
            time.sleep(10)
            #except:
             #   with open("bad_site.json","a+") as f1:
              #      f1.write(json.dumps(item,ensure_ascii=False) + "\n")
get_id_name()