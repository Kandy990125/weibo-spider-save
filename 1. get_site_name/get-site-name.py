# -*- coding: UTF-8 -*-
import requests
import json
import re
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'SCF=Ar4oR3lJRj0Q2mv3eYhQp3iy6ienei7IwnvUDmBT4kmkwwyjA9LSEgrgiDiO7XRs42LcfqyK2HXNnZvEOIyBAxw.; SUHB=0IIFWxCqd6Svuh;',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
def get_site_name():
    url = "https://m.weibo.cn/statuses/extend?id=4328304901298403"
    rep = requests.get(url,headers=headers).text
    s_list = json.loads(rep)["data"]["longTextContent"]
    list = re.findall(r"@(.+?)</a>", s_list)
    site_list = []
    bad_list = []
    for data in list:
        if data=="林彦俊":
            continue
        dir = {}
        dir["name"] = data.encode("utf-8").decode("utf-8")
        site_url = get_site_url(data)
        if site_url==200:
            bad_list.append(dir)
        else:
            dir["url"] = site_url
            site_list.append(dir)
    with open("site_name.json","a+") as f1:
        f1.write(json.dumps(site_list,ensure_ascii=False))
    with open("bad_site_name.json","a+") as f2:
        f2.write(json.dumps(bad_list,ensure_ascii=False))

def get_site_url(name):
    # name = "/n/HeartFlutter0824·林彦俊"
    url = "https://m.weibo.cn/n/" + name
    response = requests.get(url)
    url_name = str(response.url).split('/')[4]
    try:
        url_int = int(url_name)
        return response.url
    except:
        return 200

get_site_name()