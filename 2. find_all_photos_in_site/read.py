# -*- coding: UTF-8 -*-

with open("new.txt","r") as f:
    with open("m.txt","a+") as f1:
        lines = f.readlines()
        for line in lines:
            f1.write(line[1:-2]+",")