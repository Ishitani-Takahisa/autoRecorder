# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt
import json

#自作
from createRecord.countWhite import countWhite
from createRecord.borderDetect import cr_borderDetect as borderDetect
from createRecord.vsAreaDetect import vsAreaDetect
from createRecord.isPuyoColor import field2array,next2array
from createRecord.detectStartingTime import detectStartingTime
from createRecord.detectOneGame import detectOneGame


from createRecord.extractColor import extractColor

#遊び
from view_field import viewAll
from createRecord.img2points import img2points
from createRecord.detectNextChange import detectNextChange

with open("./current.json") as f:
    current = json.load(f)

with open("./vs_setting/"+current["title"]+".json") as f:
    setting = json.load(f)

with open("./area.json") as f:
    area = json.load(f)

s = detectStartingTime(setting["fps"])
print("start : ",s)
e = detectOneGame(setting,area,s)
print("end : ",e)
c = detectNextChange(s,e,area["next"])
print(s,e,c)

# img = cv2.imread("./tmp/10608.png")
# test = [9657, 9680, 9707, 9733, 9758, 9784, 9809, 9833, 9861, 9884, 9907, 9934, 9958, 9979, 10000, 10037, 10078, 10090, 10113, 10156, 10196, 10221, 10249, 10348, 10373, 10594, 10608]

# img = cv2.imread('./tmp/9733.png')

# _,field = field2array(img,area)
# points = img2points(img,area)
# print(points)
# viewAll(field,points)


