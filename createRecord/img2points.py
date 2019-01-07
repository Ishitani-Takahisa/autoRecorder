# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
import json

def patternMatch(img,template):
    """パターンマッチングを行う．大きさが異なると駄目
    
    Parameters
    ----------
    img : cv2.imread
        探す元の画像
    template : cv2.imread(".png",0)
        検索する画像
    
    Returns
    -------
    array
        [[x,y]]で存在した位置を返す
        xyの順番はこれだったか覚えてない
    """

    w, h = template.shape[::-1]
    threshold = 0.9

    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    ##扱いやすいよう、リストにし、x座標を基にソートして返す
    return sorted(list(zip(*loc[::-1])))

def img2points(img,area):
    #2gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgs = [
        img[area['points']['top']:area['points']['top']+area['points']['height'],area['points']['1p']:area['points']['1p']+area['points']['width']],
        img[area['points']['top']:area['points']['top']+area['points']['height'],area['points']['2p']:area['points']['2p']+area['points']['width']]
    ]
    points_array = [[],[]]
    points = [0,0]
    pts_threshold = 10
    for p in range(2):
        for i in range(10):
            pts = patternMatch(imgs[p],cv2.imread('./images/'+str(i)+'.png',0))
            #同じ数字を取得している部分を除去する
            for j in range(len(pts)):
                #前の要素と近すぎないものを獲得する
                if j == 0 or pts[j][0] - pts[j-1][0] > pts_threshold:
                    #tupleをlistにしてからマッチングに用いた数字を追加して得点に入れる
                    points_array[p].append([*list(pts[j]),i])
        points_array[p] = sorted(points_array[p])
        digit = 8
        #正常に取得されている
        if len(points_array[p]) == digit:
            for i in range(digit):
                points[p] += pow(10,digit - i - 1) * int(points_array[p][i][2])
        elif len(points_array[p]) == 0:
            if __name__ == "__main__":
                print("数字が一つも見当たりません")
            points[p] = -1
        else:
            # if __name__ == "__main__":
            # print(p,'が',len(points_array[p]),"桁しか取れてない",points_array[p])
            # print(points_array[p])
            points[p] = -9
    return points

def img2plot(img,area):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgs = [
        img[area['points']['top']:area['points']['top']+area['points']['height'],area['points']['1p']:area['points']['1p']+area['points']['width']],
        img[area['points']['top']:area['points']['top']+area['points']['height'],area['points']['2p']:area['points']['2p']+area['points']['width']]
    ]
    pts = []
    pts2 = []
    x = []
    y = []
    x2 = []
    y2 = []
    v_line = []
    # is_v_line = False
    is_plot_circle = not True
    is_plot_result = not False
    # 1pなら0 2pなら1
    player = 1
    for i in range(10):
        tmp = patternMatch(imgs[player],cv2.imread('./images/'+str(i)+'.png',0))
        if tmp != []:
            pts.extend(tmp)

    #同じ数字を取得している部分を除去する
    for j in range(len(pts)):
        #前の要素と近すぎないものを獲得する
        if j == 0 or pts[j][0] - pts[j-1][0] > 10:
            pts2.append(pts[j])

    for pt in pts:
        x.append(pt[0])
        y.append(pt[1])
    
    for pt in pts2:
        x2.append(pt[0])
        y2.append(pt[1])
        v_line.extend([pt[0]-10,pt[0]+10])

    print(pts2)
    fig = plt.figure().add_subplot(1,1,1)
    fig.set_xlabel('X coordinate')
    fig.set_ylabel('Y coordinate')
    # if is_v_line:
    #     fig.vlines(v_line, 10, 20, linestyles="dashed")
    if is_plot_circle:
        for pt in pts2:
            circle = plt.Circle((pt[0],pt[1]),10,fc="#999999")
            fig.add_patch(circle)
    plt.xlim([0,300])
    plt.ylim([0,30])
    if is_plot_result:
        fig.plot(x2, y2, 'o')
    else:
        fig.plot(x, y, 'o')

    plt.show()

# plt.imshow(img)
# plt.show()
