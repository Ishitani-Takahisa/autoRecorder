#!/usr/bin/python
# -*- Coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
from createRecord.img2points import img2points,patternMatch
import json
with open("./current.json") as f:
    current = json.load(f)
    area = current["area"]

def detectRensa(start,end,player):
    pn = 0 if player == "1p" else 1
    rensa_frame_list = []
    frame_list = []
    point_list = []
    total_point = 0
    for i in range(start,end):
        match = patternMatch(cv2.cvtColor(cv2.imread("./tmp/"+str(i)+".png"),cv2.COLOR_BGR2GRAY)[area['points']['top']:area['points']['top']+area['points']['height'],area['points'][player]:area['points'][player]+area['points']['width']],cv2.imread("./images/x.png",0))
        # match = match if len(match) != 0 else patternMatch(cv2.cvtColor(cv2.imread("./tmp/"+str(i)+".png"),cv2.COLOR_BGR2GRAY)[area['points']['top']:area['points']['top']+area['points']['height'],area['points'][player]:area['points'][player]+area['points']['width']],cv2.imread("./images/x2.png",0))
        if len(match) != 0:
            rensa_frame_list.append(i)
    # 連続した要素を削除する
    for frame in rensa_frame_list:
        if frame-1 not in rensa_frame_list:
            frame_list.append(frame)
            point_list.append(img2points(cv2.imread("./tmp/"+str(frame-1)+".png"),area)[pn]-total_point)
            total_point += point_list[-1]
    # 連鎖終了時の得点を追加する
    point_list.append(img2points(cv2.imread("./tmp/"+str(end)+".png"),area)[pn]-total_point)
    total_point += point_list[-1]
    return {
        "timig" : frame_list,
        "point" : point_list,
        "rensa_point" : total_point-point_list[0],
        "count" : len(frame_list)
    }

def patternMatchMAX(img,template):
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    return np.amax(res)
    # loc = np.where(res >= threshold)
    
    ##扱いやすいよう、リストにし、x座標を基にソートして返す
    # return sorted(list(zip(*loc[::-1])))


if __name__ == "__main__":
    # print(detectRensa(15279,15725,"1p"))

    # print(
    #     patternMatchMAX(cv2.cvtColor(cv2.imread("./tmp/"+str(15295)+".png"),cv2.COLOR_BGR2GRAY)[area['points']['top']:area['points']['top']+area['points']['height'],area['points']['1p']:area['points']['1p']+area['points']['width']],cv2.imread("./images/x2.png",0))
    # )
    fig = plt.figure().add_subplot(1,1,1)
    x = []
    y = []
    player = "1p"
    for i in range(15279,15725):
        x.append(i)
        y.append(patternMatchMAX(cv2.cvtColor(cv2.imread("./tmp/"+str(i)+".png"),cv2.COLOR_BGR2GRAY)[area['points']['top']:area['points']['top']+area['points']['height'],area['points'][player]:area['points'][player]+area['points']['width']],cv2.imread("./images/x.png",0)))
    
    fig.set_xlabel('frame')
    fig.set_ylabel('degree of similarity')
    plt.xlim([15279,15725])
    plt.ylim([0,1])
    fig.plot(x, y)
    plt.show()
    # cv2.imwrite("./rensa.png",)
   
   
    # plt.imshow(cv2.cvtColor(cv2.imread("./tmp/"+str(15295)+".png"),cv2.COLOR_BGR2GRAY)[area['points']['top']:area['points']['top']+area['points']['height'],area['points']['1p']:area['points']['1p']+area['points']['width']])
    # plt.show()