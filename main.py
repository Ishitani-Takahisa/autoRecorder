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
from createRecord.detectStartingTime import detectStartingTime , detectEndTime
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

def save(current):
    with open("./current.json","w") as f:
        json.dump(current,f,ensure_ascii=False)

def main():
    #試合の区切りを見つける
    if "game_list" not in current:
        #試合開始時間を入れる配列
        game_list = []
        #ゲーム開始時間を見つける
        f = detectStartingTime(setting["fps"])
        e = detectEndTime(setting["fps"],setting["f_count"])
        print("ゲーム開始時間を見つけました．フレーム : ",f)
        print("ゲーム終了時間を見つけました．フレーム : ",e)

        #"area"がなければ見つける
        if "area" not in current:
            current["area"] = borderDetect(cv2.imread('./tmp/'+str(f)+'.png'))
            area = current["area"]
            # rgb_img = cv2.imread('./tmp/'+str(f)+'.png')
            # # 枠線つける
            # #field
            # v_img = cv2.rectangle(rgb_img,(area["field"]["1p"],area["field"]["top"]),(area["field"]["1p"]+area["field"]["width"],area["field"]["top"]+area["field"]["height"]),(255,0,0),5)
            # v_img = cv2.rectangle(rgb_img,(area["field"]["2p"],area["field"]["top"]),(area["field"]["2p"]+area["field"]["width"],area["field"]["top"]+area["field"]["height"]),(0,0,255),5)
            # #next
            # v_img = cv2.rectangle(rgb_img,(area["next"]["1p"],area["next"]["top"]),(area["next"]["1p"]+area["next"]["width"],area["next"]["top"]+area["next"]["height"]),(255,0,0),5)
            # v_img = cv2.rectangle(rgb_img,(area["next"]["2p"],area["next"]["top"]),(area["next"]["2p"]+area["next"]["width"],area["next"]["top"]+area["next"]["height"]),(0,0,255),5)
            # #wnext
            # v_img = cv2.rectangle(rgb_img,(area["wnext"]["1p"],area["wnext"]["top"]),(area["wnext"]["1p"]+area["wnext"]["width"],area["wnext"]["top"]+area["wnext"]["height"]),(255,0,0),5)
            # v_img = cv2.rectangle(rgb_img,(area["wnext"]["2p"],area["wnext"]["top"]),(area["wnext"]["2p"]+area["wnext"]["width"],area["wnext"]["top"]+area["wnext"]["height"]),(0,0,255),5)
            # #points
            # v_img = cv2.rectangle(rgb_img,(area["points"]["1p"],area["points"]["top"]),(area["points"]["1p"]+area["points"]["width"],area["points"]["top"]+area["points"]["height"]),(255,0,0),5)
            # v_img = cv2.rectangle(rgb_img,(area["points"]["2p"],area["points"]["top"]),(area["points"]["2p"]+area["points"]["width"],area["points"]["top"]+area["points"]["height"]),(0,0,255),5)
            # plt.imshow(v_img)
            # plt.show()
            save(current)
        while f < e:
            print(f,len(game_list))
            f = detectOneGame(setting,current["area"],f)
            game_list.append(f)
        current["game_list"] = game_list
        save(current)
    # if "tumo_timing" not in current or ("tumo_timing" in current and len(current["tumo_timig"]) == current["game_list"]):
    #     start = 0 if "tumo_timing" not in current else len(current[])

# print(setting)
main()

    
