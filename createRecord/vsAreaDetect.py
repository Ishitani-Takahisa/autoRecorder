import numpy as np
from createRecord.extractColor import extractColor
from createRecord.countWhite import countWhite

def vsAreaDetect(img):
    lower_bg = np.array([105,100,100])
    upper_bg = np.array([120,255,255])
    ex_img = extractColor(img,lower_bg,upper_bg)
    shape = img.shape

    white = countWhite(ex_img,{"x" : 0,"y" : 0},{"x" : shape[1],"y" : shape[0]})

    minX = shape[1]
    maxX = 0

    listY = []
    #上部背景を追加する
    for k,v in white["x"].items():
        if v > (shape[0] / 2):
            listY.append(int(k))

    for i in range(shape[1]):
        if minX == i-1:
            break
        elif ex_img[listY[0],i] == 255:
            w = 0
            b = 0
            for y in listY:
                if ex_img[y,i] == 0:
                    b+=1
                else:
                    w+=1
            if b < w:
                minX = i
                break
    for i in range(shape[1]):
        if maxX == shape[1] - i:
            break
        elif ex_img[listY[0],shape[1] - 1 - i] == 255:
            w = 0
            b = 0
            for y in listY:
                if ex_img[y,shape[1] - 1 - i] == 0:
                    b+=1
                else:
                    w+=1
            if b < w:
                maxX = shape[1] - i-1
                break

    minY = listY[0]
    maxY = minY + (maxX - minX)*0.65
    
    return {
        "minX" : int(minX),
        "maxX" : int(maxX),
        "minY" : int(minY),
        "maxY" : int(maxY)
    }
