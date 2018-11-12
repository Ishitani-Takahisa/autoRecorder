import numpy as np
from createRecord.extractColor import extractColor

###test
from matplotlib import pyplot as plt
import cv2

def field2array(img,area):

    """画像とフィールドの範囲を受け取って，各マスに何色のぷよがあるかを確率として返す．

    Parameters
    ----------
    area : dict
        {
            "field":{
                "top":基準となる座標 i,
                "1p":基準となる座標 j,
                "2p":基準となる座標 j,
                "height:範囲の高さ,
                "width":範囲の幅
            },
            "next":{},
            "wnext"{}

        }
    
    Returns
    -------
    dict
        {
            "field":{
                "1p":[y][x]にkey==colorのdict,
                "2p"
            },
            "next":{},
            "wnext":{}
        }
    """


    #色の設定
    C_IMG = {
        "RED":extractColor(img,np.array([50,100,100]),np.array([70,255,255])),
        "GREEN":extractColor(img,np.array([50,100,100]),np.array([70,255,255])),
        "BLUE":extractColor(img,np.array([50,100,100]),np.array([70,255,255])),
        "YELLOW":extractColor(img,np.array([50,100,100]),np.array([70,255,255])),
        "PURPLE":extractColor(img,np.array([50,100,100]),np.array([70,255,255])),
        "OJAMA":extractColor(img,np.array([50,100,100]),np.array([70,255,255]))
    }
    C_LEN = len(C_IMG)

    #test
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def isPuyoColor(area):
        """ある範囲に存在するぷよの色を特定する
        
        Parameters
        ----------
        area : dict
            {
                "top":基準となる座標 i,
                "left":基準となる座標 j,
                "height:範囲の高さ,
                "width":範囲の幅
            }
        
        Returns
        -------
        dict
            何%で色が存在するか示す配列
            {
                "RED":0,
                "GREEN":0,
                "BLUE":81,
                "YELLOW":0,
                "PURPLE":2,
                "OJAMA":1
            }
        """

        p = {
            "RED":0,
            "GREEN":0,
            "BLUE":0,
            "YELLOW":0,
            "PURPLE":0,
            "OJAMA":0
        }
        #step : 実行時間削減のため
        step = 3
        for c in p:
            for i in range(area["top"],area["top"]+area["height"],step):
                for j in range(area["left"],area["left"]+area["width"],step):
                    if C_IMG[c][i,j] == 255:
                        p[c]+=1
            #色のあった数を面積で割ることで百分率にする
            p[c] = round(p[c]/(area["width"]*area["height"])*100*step*step)
        return p

    #分割数を設定
    sep = {
        "field":{
            "x":6,
            "y":12
        },
        "next":{
            "x":1,
            "y":2
        },
        "wnext":{
            "x":1,
            "y":2
        }
    }

    p = {
        "field":{
            "1p":[[{} for i in range(6)] for j in range(12)],
            "2p":[[{} for i in range(6)] for j in range(12)]
        },
        "next":{
            "1p":[[{}] for j in range(2)],
            "2p":[[{}] for j in range(2)]
        },
        "wnext":{
            "1p":[[{}] for j in range(2)],
            "2p":[[{}] for j in range(2)]
        }
    }

    for key in area:
        width = int(area[key]["width"]/sep[key]["x"])
        height = int(area[key]["height"]/sep[key]["y"])
        print(height,"高さ",width,"横幅")

        for i in range(0,sep[key]["y"]):
            for j in range(0,sep[key]["x"]):
                p[key]["1p"][i][j] = isPuyoColor({
                    "top":area[key]["top"]+i*height,
                    "left":area[key]["1p"]+j*width,
                    "width":width,
                    "height":height
                })
                p[key]["2p"][i][j] = isPuyoColor({
                    "top":area[key]["top"]+i*height,
                    "left":area[key]["2p"]+j*width,
                    "width":width,
                    "height":height
                })
    return p