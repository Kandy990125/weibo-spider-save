# -*- coding: UTF-8 -*-
with open("new.json","r") as f:
    s = f.readlines()[0].encode('latin-1').decode('unicode_escape')
with open("new2.json","a+") as f2:
    f2.write(s)