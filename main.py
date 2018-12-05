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
    print(setting)

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
        e = detectEndTime(setting["fps"],setting["f_count"]-1)
        print("ゲーム開始時間を見つけました．フレーム : ",f)
        print("ゲーム終了時間を見つけました．フレーム : ",e)

        #"area"がなければ見つける
        if "area" not in current:
            current["area"] = borderDetect(cv2.imread('./tmp/'+str(f)+'.png'))
            area = current["area"]
            save(current)
        while f < e - 10*setting["fps"]:
            print(f,len(game_list))
            f = detectOneGame(setting,current["area"],f)
            game_list.append(f)
        current["game_list"] = game_list
        save(current)
    if "tumo_timing" not in current:
        current["tumo_timing"] = []
        # print("asasasahluisa",current["tumo_timing"],len(current["tumo_timing"]),len(current["game_list"]))
    if len(current["tumo_timing"]) != len(current["game_list"])-1:
        for i in range(len(current["tumo_timing"]),len(current["game_list"])-1):
            print("i",i,current["game_list"][i],current["game_list"][i+1])
            current["tumo_timing"].append(detectNextChange(current["game_list"][i],current["game_list"][i+1],current["area"]["next"]))
            save(current)
    if "tumo_timing_point" not in current:
        current["tumo_timing_point"] = []
        # current["tumo_color"] = []
    if len(current["tumo_timing"]) != len(current["tumo_timing_point"]):
        for i in range(len(current["tumo_timing_point"]),len(current["tumo_timing"])):
            current["tumo_timing_point"].append({
                "1p": [],
                "2p": []
            })
            # current["tumo_color"].append([])
            #多くツモる方のネクストを参照してネクストの記録を作る
            # larger_player = "1p" if len(current["tumo_timing"]["1p"]) > len(current["tumo_timing"]["2p"]) else "2p"
            for player in current["tumo_timing"][i]:
                for frame in current["tumo_timing"][i][player]:
                    current["tumo_timing_point"][i][player].append(img2points(cv2.imread('./tmp/'+str(frame)+'.png'),current["area"]))
                    # if player == larger_player:
                    #     current["tumo_color"][i].
            save(current)


main()

    
