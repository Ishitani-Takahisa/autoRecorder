# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt
import json

img = cv2.imread('./test/sample.jpg')
with open('./test/area.json') as f:
    area = json.load(f)

#分割数を設定
sep = {
    "field":{
        "x":6,
        "y":12
    },
    "next":{
        "x":1,
        "y":2
    }
}

key = input("key : ")
i = input("i")
j = input("j")