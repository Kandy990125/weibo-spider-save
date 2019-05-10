# -*- coding: UTF-8 -*-
import json
with open("zuizhong.json","rb") as f:
    text = f.read()
    json_list = json.loads(text)
    i = 0
    for item in json_list:
        for data in  item["info"]:
            i = i + len(data["pics"])
    print(i)