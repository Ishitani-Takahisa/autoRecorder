import numpy as np
from createRecord.extractColor import extractColor

###test
from matplotlib import pyplot as plt
import cv2

img = cv2.imread("./sample125689x.png")
template = cv2.imread("./RED.png")
threshold = 0.5

res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
loc = sorted(list(zip(*np.where(res >= threshold)[::-1])))

# w, h = img.shape[::-1]

# for y in range(h):
#     for x in range(w):
#         if loc[]
for i in range(len(loc)):
    print(i,"/",len(loc),loc[i],loc[i-1],pow(loc[i][0]-loc[i-1][0],2),pow(loc[i][1]-loc[i-1][1],2))
    if i != 0 or pow(loc[i][0]-loc[i-1][0],2)+pow(loc[i][1]-loc[i-1][1],2) > 10:
        print(loc[i])