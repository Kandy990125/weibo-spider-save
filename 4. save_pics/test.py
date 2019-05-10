# -*- coding: UTF-8 -*-
import requests
import pathlib
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}
# 这是一个图片的url
url = 'https://wx1.sinaimg.cn/large/006KkQkOgy1fxuwo8jqmij323u35sqv5.jpg'
response = requests.get(url,headers=headers)
# 获取的文本实际上是图片的二进制文本
img = response.content
# 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
print(pathlib.Path("D:\\pics\\my").exists())
#with open( 'd:/pics/my/a.jpg','ab' ) as f:
#    f.write(img)