import numpy as np
import cv2
from matplotlib import pyplot as plt

#自作
from createRecord.countWhite import countWhite
from createRecord.borderDetect import cr_borderDetect as borderDetect
from createRecord.vsAreaDetect import vsAreaDetect
from createRecord.isPuyoColor import field2array

#遊び
import time

plt.gray()

#動画に対して本来は外部のjsonなどで自身で設定して読み込む項目
SCREEN_ONLY = True

def nextPuyoDetect(img,bR,bB):
    #枠の間にネクストぷよがあるはずなので
    #1p red
    if bR["minX"] < bB["minX"]:
        min


img = cv2.imread("./test4.png")
#ゲームの枠で切り抜く
game_frame = vsAreaDetect(img)
if not SCREEN_ONLY:
    img = img[game_frame["minY"]:game_frame["maxY"],game_frame["minX"]:game_frame["maxX"]]
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#BGR
# lower_blue = np.array([108,50,50])
# upper_blue = np.array([130,255,255])
lower_green = np.array([50,100,100])
upper_green = np.array([70,255,255])

lower = np.array([178,130,128])
upper = np.array([180,255,255])

# 2hsv
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# make mask
img_mask = cv2.inRange(hsv_img, lower_green, upper_green)
# extract from mask
img_color = cv2.bitwise_and(rgb_img, rgb_img, mask=img_mask)


# 指定した色に基づいたマスク画像の生成
# img_mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)
img_mask = cv2.inRange(hsv_img, lower, upper)
# img_mask = cv2.inRange(hsv_img, lower_frame_r, upper_frame_r)

# 枠見つける
area = borderDetect(img)
# 枠線つける
#field
# v_img = cv2.rectangle(rgb_img,(area["field"]["1p"],area["field"]["top"]),(area["field"]["1p"]+area["field"]["width"],area["field"]["top"]+area["field"]["height"]),(255,0,0),5)
# v_img = cv2.rectangle(rgb_img,(area["field"]["2p"],area["field"]["top"]),(area["field"]["2p"]+area["field"]["width"],area["field"]["top"]+area["field"]["height"]),(0,0,255),5)
# #next
# v_img = cv2.rectangle(rgb_img,(area["next"]["1p"],area["next"]["top"]),(area["next"]["1p"]+area["next"]["width"],area["next"]["top"]+area["next"]["height"]),(255,0,0),5)
# v_img = cv2.rectangle(rgb_img,(area["next"]["2p"],area["next"]["top"]),(area["next"]["2p"]+area["next"]["width"],area["next"]["top"]+area["next"]["height"]),(0,0,255),5)
# #wnext
# v_img = cv2.rectangle(rgb_img,(area["wnext"]["1p"],area["wnext"]["top"]),(area["wnext"]["1p"]+area["wnext"]["width"],area["wnext"]["top"]+area["wnext"]["height"]),(255,0,0),5)
# v_img = cv2.rectangle(rgb_img,(area["wnext"]["2p"],area["wnext"]["top"]),(area["wnext"]["2p"]+area["wnext"]["width"],area["wnext"]["top"]+area["wnext"]["height"]),(0,0,255),5)

# plt.imshow(v_img)
# plt.show()

p = field2array(img,area)
for i in range(12):
    for j in range(6):
        if p["field"]["1p"][i][j]["RED"] > 5:
            print(i,j,p["field"]["1p"][i][j]["RED"])

# for i in range(10):
#     time.sleep(0.1)
#     print("\007")

plt.imshow(img_mask)
plt.show()
# nextPuyoDetect(img,bR,bB)

# vImg = cv2.rectangle(cImg,(point["LT"][0],point["LT"][1]),(point["RB"][0],point["RB"][1]),(0,0,255),10)
# lower_frame_b = np.array([90,100,100])
# upper_frame_b = np.array([105,200,250])

# v_img = extractColor(img,lower_frame_b,upper_frame_b)

#gray = extractColor(rgb_img,lower_green,upper_green)
