# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt
import json

#自作
from createRecord.countWhite import countWhite
from createRecord.borderDetect import cr_borderDetect as borderDetect
from createRecord.vsAreaDetect import vsAreaDetect
from createRecord.isPuyoColor import field2array


from createRecord.extractColor import extractColor

#遊び
import time
from view_field import viewAll
from createRecord.img2points import img2points
# from createRecord.findNextChange import findNextChange

plt.gray()

#動画に対して本来は外部のjsonなどで自身で設定して読み込む項目
SCREEN_ONLY = True


# img = cv2.imread('./test/sample.jpg')
img = cv2.imread("./tmp/14370.png")

# plt.imshow(img)
# plt.show()
#ゲームの枠で切り抜く
# game_frame = vsAreaDetect(img)
# if not SCREEN_ONLY:
    # img = img[game_frame["minY"]:game_frame["maxY"],game_frame["minX"]:game_frame["maxX"]]
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # 枠見つける
# area = borderDetect(img)
# with open('./test/area.json','w') as f:
#     json.dump(area,f,ensure_ascii=False)

with open('./current.json') as f:
    area = json.load(f)["area"]

# print(findNextChange(7115,8671,area["next"]))

# 枠線つける
#field
v_img = cv2.rectangle(rgb_img,(area["field"]["1p"],area["field"]["top"]),(area["field"]["1p"]+area["field"]["width"],area["field"]["top"]+area["field"]["height"]),(255,0,0),10)
v_img = cv2.rectangle(rgb_img,(area["field"]["2p"],area["field"]["top"]),(area["field"]["2p"]+area["field"]["width"],area["field"]["top"]+area["field"]["height"]),(0,0,255),10)
#next
v_img = cv2.rectangle(rgb_img,(area["next"]["1p"],area["next"]["top"]),(area["next"]["1p"]+area["next"]["width"],area["next"]["top"]+area["next"]["height"]),(255,0,0),10)
v_img = cv2.rectangle(rgb_img,(area["next"]["2p"],area["next"]["top"]),(area["next"]["2p"]+area["next"]["width"],area["next"]["top"]+area["next"]["height"]),(0,0,255),10)
#wnext
v_img = cv2.rectangle(rgb_img,(area["wnext"]["1p"],area["wnext"]["top"]),(area["wnext"]["1p"]+area["wnext"]["width"],area["wnext"]["top"]+area["wnext"]["height"]),(255,0,0),10)
v_img = cv2.rectangle(rgb_img,(area["wnext"]["2p"],area["wnext"]["top"]),(area["wnext"]["2p"]+area["wnext"]["width"],area["wnext"]["top"]+area["wnext"]["height"]),(0,0,255),10)
#points
# v_img = cv2.rectangle(rgb_img,(area["points"]["1p"],area["points"]["top"]),(area["points"]["1p"]+area["points"]["width"],area["points"]["top"]+area["points"]["height"]),(255,0,0),10)
# v_img = cv2.rectangle(rgb_img,(area["points"]["2p"],area["points"]["top"]),(area["points"]["2p"]+area["points"]["width"],area["points"]["top"]+area["points"]["height"]),(0,0,255),10)

# C_IMG = {
#     "RED":extractColor(img,np.array([178,130,128]),np.array([180,255,255])),
#     "GREEN":extractColor(img,np.array([50,100,100]),np.array([70,255,255])),
#     "BLUE":extractColor(img,np.array([100,50,50]),np.array([120,255,255])),
#     "YELLOW":extractColor(img,np.array([20,50,230]),np.array([30,255,255])),
#     "PURPLE":extractColor(img,np.array([130,50,180]),np.array([140,255,255])),
#     "OJAMA":extractColor(img,np.array([0,0,0]),np.array([250,10,230]))
# }
# C_LEN = len(C_IMG)
# #aa
# for color in C_IMG:
#     cv2.imwrite(color+".png",C_IMG[color])

# cv2.imwrite("_border.png",cv2.cvtColor(v_img, cv2.COLOR_BGR2RGB))
lower_frame_r = np.array([165,60,160])
upper_frame_r = np.array([180,150,255])
ex_img = extractColor(img,np.array([165,60,160]),np.array([180,150,255]))
# plt.imshow(ex_img)
# plt.show()
cv2.imwrite("border_white.png",ex_img)
# _,field = field2array(img,area)
# points = img2points(img,area)
# viewAll(field,points)

# for i in range(12):
#     for j in range(6):
#         if p2["field"]["1p"][i][j]:
#             print(i,j,p2["field"]["1p"][i][j])
# view_field()

# viewField(p2)
# for i in range(10):
#     time.sleep(0.1)
#     print("\007")

# plt.imshow(img_mask)
# plt.show()
# nextPuyoDetect(img,bR,bB)

# vImg = cv2.rectangle(cImg,(point["LT"][0],point["LT"][1]),(point["RB"][0],point["RB"][1]),(0,0,255),10)
# lower_frame_b = np.array([90,100,100])
# upper_frame_b = np.array([105,200,250])

# v_img = extractColor(img,lower_frame_b,upper_frame_b)

#gray = extractColor(rgb_img,lower_green,upper_green)
