# -*- coding:utf8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
import json

# テスト用
import subprocess

# detectoperateから
def in3DArray(x,ary):
    """
    3次元配列aryの中に配列xを要素として持つ2次元配列があるかを確認する
    
    Parameters
    ----------
    x : ary
        探す配列x
    ary : ary
        探す元となる配列
    Returns
    -------
    Boolean
        存在したかどうか．
    """
    
    for i in range(len(ary)):
        if x in ary[i]:
            return True
    return False

def copy2DArray(ary):
    """
    二次元配列をシャローコピーする
    
    Parameters
    ----------
    ary : ary
        コピー元の配列
    Returns
    -------
    ary
        コピーした配列
    """
    a = []
    for i in range(len(ary)):
        a.append(ary[i][:])
    return a

def check_can_put(field):
    """
    フィールドを確認し，置ける位置を[x][r]の配列で返す
    
    Parameters
    ----------
    field : ary
        確認する対戦フィールド
    Returns
    -------
    ary
        置けるかどうかを[x][r]でアクセス出来る配列
    """

    #どこに置けるかを示す配列，置けないことが判明したらfalseを与える
    canput = [[True for i in range(4)] for j in range(6)]

    #1番上の段が埋まっているかの確認(縦置き)
    for i in range(6):
        # 0がnull field[0] == 13段目
        if field[0][i] != 'NULL':
            if i == 0 or i == 5:
                canput[i][2] = canput[i][0] = False
            if i == 1:
                canput[i][2] = canput[i][0] = canput[i-1][2] = canput[i-1][0] = False
            if i == 3:
                canput[i][2] = canput[i][0] = canput[i+1][2] = canput[i+1][0] = canput[i+2][2] = canput[i+2][0] = False
            if i == 4:
                canput[i][2] = canput[i][0] = canput[i+1][2] = canput[i+1][0] = False
        # 軸ぷよは14段にならない
        if field[1][i] != 'NULL':
            canput[i][2] = False

    small = -1
    big = 6

    #2(中心)より小さい列と大きい列でそれぞれ12段目が埋まっているか確認する
    #2に近い場所が壁（超えられない）
    for i in range(6):
        if field[1][i] != 'NULL':
            if i < 2:
                small = small if i < small else i
            else:
                big = i if i < big else big
    
    #壁を超えるための足がかりとなる11段目が内部にあるか？
    asiba = False
    for i in range(small+1,big):
        if field[2][i] != 'NULL':
            asiba = True

    #足場がない場合は壁を超えられない
    if asiba is False:
        for i in range(6):
            #あとで直す
            if (small != -1 and i <= small) or (big != 6 and big <= i):
                canput[i][0] = canput[i][2] = False

    for i in range(6):
        #r == 1を考える
        if i < 5 and not canput[i+1][0]:
            canput[i][1] = False
        else:
            canput[i][1] = canput[i][0]
        #r == 3
        if i > 0 and not canput[i-1][0]:
            canput[i][3] = False
        else:
            canput[i][3] = canput[i][0]

    # 端を超えて回転させれない
    canput[0][3] = canput[5][1] = False
    return canput

def view_field(field):
    print("---------------")
    for i in range(13):
        sys.stdout.write("| ")
        for j in range(6):
            # sys.stdout.write(str(i)+str(j)+" ")
            puyo = field[i][j]
            if puyo is 0:
                sys.stdout.write("  ")
            elif puyo is 1:
                sys.stdout.write(pycolor.RED + "● " + pycolor.END)
            elif puyo is 2:
                sys.stdout.write(pycolor.BLUE + "● " + pycolor.END)
            elif puyo is 3:
                sys.stdout.write(pycolor.YELLOW + "● " + pycolor.END)
            elif puyo is 4:
                sys.stdout.write(pycolor.PURPLE + "● " + pycolor.END)

        sys.stdout.write("|\n")
    print("---------------")

def fallPuyo(field):
    """
    対戦フィールドを受け取り，浮いているぷよを落としたフィールドを返す
    
    Parameters
    ----------
    field : ary
        対戦フィールド
    Returns
    -------
    ary
        浮いているぷよを落としたフィールド
    """
    f = copy2DArray(field)
    for i in range(6):
        space = 0
        for j in range(12,-1,-1):
            if f[j][i] is 'NULL':
                space+=1
            elif space is not 0:
                f[j+space][i] = f[j][i]
                f[j][i] = 'NULL'
    return f

def putPuyo(field,tumo,x,r):
    """
    フィールドとツモ，そのツモをどこに置くかを受け取り，置いた後のフィールドを返す
    
    Parameters
    ----------
    field : ary
        対戦フィールド
    tumo : ary
        2個1セットのぷよ
        tumo[0]とtumo[1]に色(int)が入っている
    x : int
        位置 0-5
    r : int
        回転 0-3
        1毎に時計回りに45°回転
    Returns
    -------
    ary
        操作した後のフィールドを返す．
        4連結があっても連鎖を開始する前の状態で返す
    """

    f = copy2DArray(field)
    if r is 0:
        f = fallPuyo(f)
        #2個置けるか確認して置けなかったら下側のみ置く
        if f[1][x] is 'NULL':
            f[0][x] = tumo[0]
            f[1][x] = tumo[1]
        else:
            f[0][x] = tumo[1]
    elif r is 1:
        f = fallPuyo(f)
        f[0][x] = tumo[1]
        f[0][x+1] = tumo[0]
    elif r is 2:
        # return putPuyo(f,tumo[::-1],x,0)
        f = fallPuyo(f)
        f[0][x] = tumo[1]
        f[1][x] = tumo[0]
    elif r is 3:
        f = fallPuyo(f)
        f[0][x-1] = tumo[0]
        f[0][x] = tumo[1]
    return fallPuyo(f)

def Vanish_puyo(field,chain_list):
    """
    フィールドと4連結している色の位置を受け取って消す
    消した後のフィールドを返すが，落下はさせない．
    
    Parameters
    ----------
    field : ary
        処理を行うフィールド
    chain_list : ary
        4連結以上している位置[i,j]が入った消えるリストの配列の入った配列
        要素数は別々に消える箇所の数
    Returns
    -------
    ary
        処理後のフィールド
    """

    for i in range(len(chain_list)):
        for j in range(len(chain_list[i])):
            field[chain_list[i][j][0]][chain_list[i][j][1]] = 'NULL'
    return field

#連結を確認する
def countLink(i,j,f,link):
    c = f[i][j]
    f[i][j] = -1
    link.append([i,j])
    if j > 0 and f[i][j-1] == c:
        countLink(i,j-1,f,link)
    if j < 5 and f[i][j+1] == c:
        countLink(i,j+1,f,link)
    if i > 1 and f[i-1][j] == c:
        countLink(i-1,j,f,link)
    if i < 12 and f[i+1][j] == c:
        countLink(i+1,j,f,link)
    return link

#すべての連結を確認する
def countAllLink(f):
    link = []
    for i in range(13):
        for j in range(6):
            #お邪魔ぷよではなく，連結未確認
            if f[i][j] is not 'NULL' and not in3DArray([i,j],link):
                link.append(countLink(i,j,copy2DArray(f),[]))
    return link

#連鎖が発生したか確認する．発生してたら消える連結のリストを返す
def checkOccurChain(field):
    f = copy2DArray(field)
    link = countAllLink(f)
    chain_list = []
    # print(link)
    for i in range(len(link)):
        if len(link[i]) >= 4:
            chain_list.append(copy2DArray(link[i]))
    return chain_list     

def runChain(field):
    """連鎖実行後のフィールドを返す
    
    Parameters
    ----------
    field : [6][13]
        着手後，連鎖実行前のフィールド
    
    Returns
    -------
    field : [6][13]
        連鎖実行後のフィールド
    """

    f = copy2DArray(field)
    c_list = checkOccurChain(f)
    while(c_list != []):
        f = fallPuyo(Vanish_puyo(f,c_list))
        c_list = checkOccurChain(f)
    return f



# ここから


with open("./kihu.json") as f:
    kihu = json.load(f)

players = ["1p","2p"]
class RectSetting:
    size = {
        "height" : 200,
        "width" : 200
    }
    pt = {
        "top" : 100,
        "1p": 100,
        "2p": 100+200*6*2
    }
    font = cv2.FONT_HERSHEY_COMPLEX

print(RectSetting)
    # def __init__(self,pt,size,margin):
    #     self.size = size
    #     self.pt = {
    #         "1p" : pt,
    #         "2p" : pt+size["width"]*6+margin
    #     } 

# def operate2position(operate):
#     """置いた位置から置いた座標に変える
    
#     Parameters
#     ----------
#     operate : dict
#         {
#             "x" : 軸ぷよの座標,
#             "r" : 右回転での回転数
#         }
    
#     """
#     if r == 0 or r == 2:
#         return [operate["x"],operate["x"]]
#     elif r == 1:
#         return [operate["x"],operate["x"]-1]
#     elif r == 3:
#         return [operate["x"],operate["x"]+1]

def img_init(height,width,color):
    """単色で塗りつぶした画像を返す
    
    Parameters
    ----------
    height : int
        高さ
    width : int
        幅
    color : tuple
        (B,G,R)
    
    """

    img = np.zeros((height,width,3), dtype=np.uint8)
    return cv2.rectangle(img, (0,0), (width, height), color, cv2.FILLED)
    
def rectTable(img,pt,size,x,y,color,line_height):
    for i in range(x+1):
        img = cv2.line(img,(pt["left"]+i*size["width"],pt["top"]),(pt["left"]+i*size["width"],pt["top"]+size["height"]*y),color,line_height)
    for j in range(y+1):
        img = cv2.line(img,(pt["left"],pt["top"]+j*size["height"]),(pt["left"]+x*size["width"],pt["top"]+j*size["height"]),color,line_height)
    return img

def rectFieldInit():
    img = img_init(2894,4093,(255,255,255))
    
    for player in players:
        arg_table = {
            "img" : img,
            "pt" : {
                "left" : RectSetting.pt[player],
                "top" : RectSetting.pt["top"]
            },
            "size" : RectSetting.size,
            "x" : 6,
            "y" : 13,
            "color" : (0,0,0),
            "line_height" : 5
        }
        img = rectTable(**arg_table)

    return img

def rectField(img,field,count_field):
    color = {
        "RED" : (48,32,192),
        "PURPLE" : (185,59,111),
        "YELLOW" : (48,193,248),
        "GREEN" : (43,169,33),
        "BLUE" : (163,61,19)
    }
    # img = cv2.circle(img,(200,200),90,color["RED"],-1)

    for player in players:
        for i in range(13):
            for j in range(6):
                if field[player][i][j] != "NULL":
                    img = cv2.circle(img,(RectSetting.pt[player]+round(RectSetting.size["width"]*(j+0.5)),RectSetting.pt["top"]+round(RectSetting.size["height"]*(i+0.5))),90,color[field[player][i][j]],-1)
                    if count_field[player][i][j] > 9:
                        # margin = round(RectSetting.size["width"]/4)
                        margin = 1/5
                        font_size = 3
                    else:
                        margin = 1/3
                        font_size = 3
                    img = cv2.putText(
                        img,
                        str(count_field[player][i][j]),
                        (
                            RectSetting.pt[player]+round(RectSetting.size["width"]*(j+margin)),
                            RectSetting.pt["top"]+round(RectSetting.size["height"]*(i+2/3))
                        ), RectSetting.font, font_size, (255, 255, 255), 3)
    return img


def kihu2map(kihu):
    img = rectFieldInit()

    players = ["1p","2p"]

    # for players in player:
    field = {
        "1p" : [['NULL' for i in range(6)] for j in range(13)],
        "2p" : [['NULL' for i in range(6)] for j in range(13)]
    }
    count_field = {
        "1p" : [['NULL' for i in range(6)] for j in range(13)],
        "2p" : [['NULL' for i in range(6)] for j in range(13)]  
    }

    # 連鎖が発生するか最後の一手になるまで続ける
    progress = {
        "1p" : 0,
        "2p" : 0
    }

    # 消すのを含めて処理をする必要がある
    # 1pと2p両方で処理，これが1枚の画像の処理
    for player in players:
        # 全ての棋譜を読み込むまで処理
        # for i in range(progress[player],len(kihu["puts"][player]))):
        while(checkOccurChain(field[player]) == [] and progress[player] != len(kihu["puts"][player])):
            print(progress[player],len(kihu["puts"][player]))
            field[player] = putPuyo(field[player],kihu["next_list"][progress[player]],kihu["puts"][player][progress[player]]["operate"]["x"],kihu["puts"][player][progress[player]]["operate"]["r"])
            count_field[player] = putPuyo(count_field[player],[progress[player]+1,progress[player]+1],kihu["puts"][player][progress[player]]["operate"]["x"],kihu["puts"][player][progress[player]]["operate"]["r"])
            progress[player]+=1
            # progress[player] = i

    img = rectField(img,field,count_field)
    cv2.imwrite("table.png",img)
    subprocess.call(["open","table.png"])

    # print(progress)
def main():
    img = rectFieldInit()
    img = rectField(img,[],[])
    cv2.imwrite("table.png",img)
    subprocess.call(["open","table.png"])
if __name__ == '__main__':
    # main()
    kihu2map(kihu)