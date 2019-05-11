# weibo-picture-spider-and-save

已更新到Hexo博客:[Kandy990125](https://www.evanlin.cn)

# 前言

最近想提升一下前端技能，开始学习nodejs，但是学习前端技能，想了想前端要做的网站主题，于是，一番绞尽脑汁，决定！做一个鹅子的图片分享网站。
<!--more-->
但是，网络上有那————么多的鹅子相关照片，作为一个图片分享网站，数据总得全吧，于是我开始了我最熟悉的！做！爬！虫！（逐渐跑偏），最后由于微博图床总是搞不好就会被ban掉，那么我们来把这些照片都存起来好了！
先放一张鹅子帅图（跑走）
 ![林彦俊！帅！](https://github.com/Kandy990125/images/blob/master/006WOLJIly1fzhxqagtp9j32ot1sj7wh.jpg?raw=true)

# 项目流程

 1. 从 [@星际凉茶](https://m.weibo.cn/u/1787296133?uid=1787296133&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%98%9F%E9%99%85%E5%87%89%E8%8C%B6) 姐姐的 [置顶微博](https://m.weibo.cn/status/4328304901298403?) 爬取所有站子的uid。（跑路的站子我也记在小本本上了赫赫）
 2. 爬取每个站子发布的微博，从而获得发布微博的时间，微博内容，微博ID，微博下图片的PID，json存储。
 3. 遍历每个站子的相关微博下的PID，存储到电脑中。
 4. 可以快乐开始看鹅子的照片啦！！

## step1：抓取所有站子的信息

具体代码如下，下列代码均在`Python3.7`环境下调试运行：

```Python
# -*- coding: UTF-8 -*-
import requests
import json
import re
# 虽然数据量不多，但最好加个headers，这样网页不容易被ban掉
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
# 从星际凉茶姐姐的微博中获取站子ID
def get_site_name():
	# 储存那条微博相关信息的api
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

# 由于从那条微博信息api中获得到的地址并不是真正的站子微博主页地址，所以需要再次request
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
```

以如下方式进行存储。

```Yaml
[
	{
		uname:<site_name>,
		uid:<uid>
	},{
		uname:<site_name>,
		uid:<uid>
		},...
]
```

## step2：根据微博主页URL获取包含图片的微博信息

具体代码如下：

```Python
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
    # 对于站子主页URL进行分页爬取
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
```

相关微博信息的存储格式是：

```YAML
{
  [
    {  
      uname:<site_name>,
      uid:<site_id>,
      infos:[
      {
        id:<weibo_id>,
	text:<weibo_content>,
	time:<created_time>,
	pics:[picid,picid,...]
	}
       ]
     }
   ],...
}
```

## step3：通过PID，下载图片

具体代码如下：

```Python
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
                    # 这里对图片进行一个简单筛选，有些只是站姐们的生活图片
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
```

存储结构：`D:\时间\站子名称`

## 结果展示

其实最后也没有存储4w张图片（标题党滑跪）（才不是因为自习室要关门了），所以最后按照列表只抓取了7个站子共4717张图片，占用空间大小是：8.56G，站子列表如下：
[@目下赏味·林彦俊](https://m.weibo.cn/u/6482581401)
[@Mercury0824_林彦俊个站](https://m.weibo.cn/u/6365924382)
[@ExclusionZone·林彦俊](https://m.weibo.cn/u/6484219603)
[@INITIALE·林彦俊](https://m.weibo.cn/u/6534587243")
[@DearEvan-林彦俊个站](https://m.weibo.cn/u/6522371782")
[@EtherealPlanet丨林彦俊](https://m.weibo.cn/u/6223868986")
[@惊彦FOR林彦俊](https://m.weibo.cn/u/6131013022")
![存储](https://github.com/Kandy990125/images/blob/master/my.PNG?raw=true)

![站子](https://github.com/Kandy990125/images/blob/master/site.PNG?raw=true)

# 后记

文章中所述的爬虫代码有个bug就是其中的编码问题
欢迎大家在下方评论区随时交流指正

微博：麦不辣鸡腿堡

Github：Kandy990125

E-mail：kandy990125@gmail.com
