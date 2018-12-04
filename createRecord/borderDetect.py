import cv2
import numpy as np

from createRecord.utils.my_mean import myMean
from createRecord.countWhite import countWhite
from createRecord.extractColor import extractColor

def width2field(top,left,right,player):
    # def kiriyoku(n,m):
    #     return n if n%m==0 else n+(m-n%m) if n%m>m/2 else n-n%m

    pf = {
        "left":left,
        "right":right,
    }
    while (pf["right"] - pf["left"]) % 6 != 0:
        pf["left"]+=1
        if (pf["right"] - pf["left"]) % 6 > 0:
            pf["right"]-=1

    width = pf["right"] - pf["left"]
    if width%50 != 0:
        width -= width%50
    h = round(width*1.8)
    height = h if h%12==0 else h+(12-h%12) if h%12>5 else h-h%12
    player_1_left = pf["left"] if player == 1 else pf["left"]-2*width
    field = {
            "top":top,
            "width":width,
            "height":height,
            "1p":player_1_left,
            "2p":player_1_left+2*width
        }
    n_width = round(width/6)
    _next = {
            "top":top+round(width/15),
            "width":n_width,
            "height":round(width*0.3) if round(width*0.3)%2==0 else round(width*0.3)+1,
            "1p":field["1p"]+width+round(width*2/15),
            "2p":field["2p"]-round(width*2/15)-n_width
        }
    wn_width = round(_next["width"]*0.7)
    _wnext = {
        "top":_next["top"]+_next["height"],
        "width": wn_width,
        "height": wn_width*2,
        "1p": _next["1p"]+round(0.15*field["width"]),
        "2p": _next["2p"]-round(0.1*field["width"])
    }
    _points = {
        "top": field["top"]+field["height"]+round(field["width"]/120),
        "width": field["width"],
        "height": round(field["width"]/5),
        "1p": field["1p"],
        "2p": field["2p"]
    }

    return {
        "field":field,
        "next": _next,
        "wnext": _wnext,
        "points": _points
    }



def cr_borderDetectLU(img,lC,uC):
    ex_img = extractColor(img,lC,uC)
    shape = img.shape
    white = countWhite(ex_img,{"x" : 0,"y" : 0},{"x" : shape[1],"y" : shape[0]})

    #最大値，最小値で初期化
    # minX,minY
    pointLT = [shape[1],shape[0]]
    # maxX,maxY
    pointRB = [0,0]

    # n で許容する範囲を調整する
    def getY(listX,n):
        lineY = []
        # xが多い所 == 枠の横線 , key == y
        for k,v in listX.items():
            if v > (shape[0] / n):
                lineY.append(int(k))
    
        minY = 0
        maxY = shape[0]
        meanY = myMean(lineY)
        for y in lineY:
            if meanY > y and minY < y:
                minY = y
            elif meanY < y and maxY > y:
                maxY = y
        
        # print("max = ",maxY)
        # print("min = ",minY)
        # print(shape[0])
        if maxY - minY < shape[0]*0.4:
            return getY( listX,n+0.1)
        return {
            "min" : minY,
            "max" : maxY
        }
    
    # TODO : 要調整
    # yがいっぱいあるところ見る
    def getX(listY,n):
        print(shape[1],shape[1]/n)
        lineX = []
        # yが多い所 == 枠の縦線 , key == x
        for k,v in listY.items():
            if v > 100:
                print(k,v)
            if v > shape[1] / n:
                lineX.append(int(k))
        minX = 0
        maxX = shape[1]
        length = len(listY)
        meanX = myMean(lineX)
        # print("平均",meanX)
        for x in lineX:
            if meanX > x and minX < x:
                minX = x
            elif meanX < x and maxX > x:
                maxX = x

        
        # print("maxX = ",maxX)
        # print("minX = ",minX)
        # print(shape[0])

        return {
            "min" : minX,
            "max" : maxX
        }


    y = getY(white["x"],3.5)
    x = getX(white["y"],3)

    return width2field(y["min"],x["min"],x["max"],1 if shape[1]/2 > x["max"] else 2)

def cr_borderDetect(img):
    print(img.shape)
    #make mask
    lower_frame_r = np.array([165,60,160])
    upper_frame_r = np.array([180,150,255])
    return cr_borderDetectLU(img,lower_frame_r,upper_frame_r)