#!/usr/bin/python
# -*- Coding: utf-8 -*-
import sys
import cv2
from createRecord.img2points import img2points,patternMatch
from createRecord.isPuyoColor import field2array
from detectFirstChain import detectFirstChain
from detectNextColor import detectNextColor
import json
import math

debugF = False

with open("./current.json") as f:
    current = json.load(f)
    area = current["area"]

class pycolor:
    """
    stdoutで用いる色情報保持用クラス
    """
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'

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

def view_s_field(f):
    if len(f) == 12:
        field = copy2DArray(f)
        field.insert(0,['NULL','NULL','NULL','NULL','NULL','NULL'])
    else:
        field = f
    print("---------------")
    for i in range(13):
        sys.stdout.write("| ")
        for j in range(6):
            # sys.stdout.write(str(i)+str(j)+" ")
            puyo = field[i][j]
            if puyo is 'NULL':
                sys.stdout.write("  ")
            elif puyo is 'RED':
                sys.stdout.write(pycolor.RED + "● " + pycolor.END)
            elif puyo is 'BLUE':
                sys.stdout.write(pycolor.BLUE + "● " + pycolor.END)
            elif puyo is 'YELLOW':
                sys.stdout.write(pycolor.YELLOW + "● " + pycolor.END)
            elif puyo is 'GREEN':
                sys.stdout.write(pycolor.GREEN + "● " + pycolor.END)
            elif puyo is 'PURPLE':
                sys.stdout.write(pycolor.PURPLE + "● " + pycolor.END)
            elif puyo is 'OJAMA':
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
    if j > 0 and f[i][j-1] is c:
        countLink(i,j-1,f,link)
    if j < 5 and f[i][j+1] is c:
        countLink(i,j+1,f,link)
    if i > 1 and f[i-1][j] is c:
        countLink(i-1,j,f,link)
    if i < 12 and f[i+1][j] is c:
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
def checkOccurChain(f):
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

def putSim(field,next):
    canput = check_can_put(field)
    result = []
    for x in range(6):
        for r in range(4):
            if canput[x][r]:
                result.append({
                    "position": {
                        "x":x,
                        "r":r
                    },
                    "field": putPuyo(field,next,x,r)
                })
    return result


def detect(field,nextField,next):
    """ネクストをどの位置においたのか特定する
    
    Parameters
    ----------
    field : [6][13]
        着手前のfield
    nextField : [6][12]
        着手後の取得されたフィールド，13段目は不明
    next : [2]
        ネクストの色がはいった配列
    
    Returns
    -------
    Array or Boolean
        確定出来る場合は置いた場所，出来ない場合は候補，おかしい場合は，False
    """

    candidate = []
    nFP = copy2DArray(nextField)
    nFP.insert(0,['NULL','NULL','NULL','NULL','NULL','NULL'])
    sim = putSim(field,next)
    for x in sim:
        if x["field"] == nFP:
            return x["position"]
        f12 = copy2DArray(x["field"])
        f12.pop(0)
        if f12 == nextField:
            candidate.append(x["position"])
    if len(candidate) == 0:
        if debugF:
            print("不具合↓着手前")
            view_s_field(field)
            print("ネクスト is ",next)
            view_s_field(nextField)
            print("↑着手あと")
        return False
    if len(candidate) == 1:
        return candidate[0]
    else:
        # ゾロだった場合 x,r がx0もx2も同じなので2を採用（速いので）
        # 同じく x,1とx+1,3が同じxが小さい方を採用（近いので）
        if next[0] == next[1]:            
            for i in range(6):
                # 縦置きの場合 0が☓
                if {'x': i, 'r': 0} in candidate:
                    candidate.pop(candidate.index({'x': i, 'r': 0}))
                # 横置きの場合，2が中心なので0,1の時は1が☓,2はok，3以降は3が☓
                if i<2 and {'x': i, 'r': 1} in candidate:
                    candidate.pop(candidate.index({'x': i, 'r': 1}))
                if i>2 and {'x': i, 'r': 3} in candidate:
                    candidate.pop(candidate.index({'x': i, 'r': 3}))
        
        if len(candidate) == 1:
            return candidate[0]

        return candidate

def preprocessingField(field):
    f = copy2DArray(field)
    for i in range(6):
        for j in range(0,len(field)-1):
            if f[j][i] != 'NULL' and f[j+1][i] == 'NULL':
                f[j][i] = 'NULL'
    
    return f

def isX(frame,player):
    templates = [cv2.imread("./images/x_l.png",0),cv2.imread("./images/x_l2.png",0),cv2.imread("./images/x_l3.png",0),cv2.imread("./images/x_l4.png",0),cv2.imread("./images/x_l5.png",0),cv2.imread("./images/x_front.png",0),cv2.imread("./images/x_r1.png",0),cv2.imread("./images/x_r2.png",0),cv2.imread("./images/x_r3.png",0)]
    img = cv2.cvtColor(cv2.imread('./tmp/'+str(frame)+'.png'), cv2.COLOR_BGR2GRAY)
    img = img[area["field"]["top"]:area["field"]["top"]+round(area["field"]["height"]/5),area["field"][player]+round(area["field"]["width"]/6*1.5):area["field"][player]+round(area["field"]["width"]/6*3.5)]
    for template in templates:
        match_list = patternMatch(img,template)
        if len(match_list) != 0:
            return True
    return False

def isFallPuyo(field,nextField):
    """おじゃまが降ったか確認
    
    Parameters
    ----------
    field : [13][6]
        
    nextField : [12][6]
        取得したもの
    
    Returns
    -------
    Boolean
        
    """

    f = copy2DArray(field)
    f.pop(0)
    for i in range(len(f)):
        for j in range(len(f[0])):
            if nextField[i][j] == 'OJAMA' and f[i][j] != nextField[i][j]:
                return True
    return False

def detectOperate(field,next,player,point,frame,nextFrame):
    img = cv2.imread('./tmp/'+str(nextFrame)+'.png')
    pn = 0 if player == "1p" else 1
    p = img2points(img,current["area"])[pn]
    print(p-point,"pt獲得")
    if debugF:
        print(p,point)
    is_chain = p - point >= 40
    # 連鎖が発生 == ポイント40以上獲得した場合は，最初に連鎖が発生したフレームでフィールドを確認する
    if is_chain:
        f = detectFirstChain(frame,nextFrame,current["area"]["points"],player)
        img = cv2.imread('./tmp/'+str(f)+'.png')
    else:
        f = nextFrame
    _,nextField = field2array(img,current["area"])
    nextField = nextField["field"][player]
    if isX(f,player):
        nextField[0][2] = 'NULL'
    elif debugF:
        print("Falseだよ",f)
    # 誤検知対策
    nextField = preprocessingField(nextField)
    # おじゃま落下があるか確認し，ある場合は，前処理を行う
    if isFallPuyo(field,nextField):
        pass

    candidate = detect(field,nextField,next)
    if type(candidate) is bool:
        _,nextField = field2array(img,current["area"],1000)
        nextField = nextField["field"][player]
        if isX(f,player):
           nextField[0][2] = 'NULL'
        nextField = preprocessingField(nextField)
        candidate = detect(field,nextField,next)

    # 確定出来た場合
    if type(candidate) is dict:
        return candidate,p
    elif type(candidate) is list:
        pass
    # 候補が複数存在する場合
    print("来ちゃった///")

def fieldUpDate(field,next,x,r,player,putFrame):
    f = runChain(putPuyo(field,next,x,r))
    return f

def createRecord():
    # {
    #     '1p': [14365, 14440, 14464, 14491, 14517, 14542, 14570, 14597, 14623, 14647, 14687, 14714, 14747, 14771, 14795, 14819, 14842, 14872, 14894, 14917, 14939, 14960, 14983, 15014, 15034, 15053, 15072, 15092, 15125, 15153, 15191, 15209, 15227, 15244, 15262, 15277, 15654, 15725, 15753, 15776],
    #     '2p': [14440, 14464, 14491, 14517, 14540, 14566, 14593, 14620, 14649, 14670, 14694, 14729, 14752, 14777, 14797, 14824, 14842, 14869, 14895, 14920, 14937, 14967, 14995, 15020, 15037, 15059, 15079, 15099, 15119, 15288, 15343, 15545, 15566, 15590, 15613, 15677, 15696, 15946]
    # }
    f_list = {
        "1p" : [14440, 14464, 14491, 14517, 14542, 14572, 14597, 14623, 14647, 14687, 14714, 14747, 14771, 14795,14819, 14842, 14874, 14894, 14917, 14939, 14960, 14983, 15014, 15034, 15053, 15072, 15093, 15125, 15153, 15191, 15209, 15227, 15244, 15262, 15279, 15725, 15753, 15776],
        "2p" : [14440, 14464, 14491, 14517, 14540, 14566, 14593, 14620, 14649, 14670, 14694, 14729, 14752, 14777, 14797, 14824, 14842, 14869, 14895, 14920, 14937, 14967, 14995, 15020, 15037, 15059, 15079, 15099, 15119, 15288, 15545, 15566, 15590, 15613, 15677, 15696]
    }

    if len(f_list["1p"]) > len(f_list["2p"]):
        next_list = detectNextColor(f_list["1p"],"1p")
    else:
        next_list = detectNextColor(f_list["2p"],"2p")

    field = {
        "1p" : [['NULL' for i in range(6)] for j in range(13)],
        "2p" : [['NULL' for i in range(6)] for j in range(13)]
    }

    point = {
        "1p":0,
        "2p":0
    }

    remaining_point = {
        "1p":0,
        "2p":0
    }

    prev_point = {
        "1p":0,
        "2p":0
    }

    players = ["2p","1p"]

    for player in players:
        print(player,"の記録を開始します")
        print(f_list[player])
        for i in range(len(f_list[player])-1):
            prev_point[player] = point[player]
            candidate,point[player] = detectOperate(field[player],next_list[i],player,point[player],f_list[player][i],f_list[player][i+1])
            remaining_point[player] += point[player] - prev_point[player]
            print(candidate)
            # fieldの更新
            field[player] = fieldUpDate(field[player],next_list[i],candidate["x"],candidate["r"],player,f_list[player][i])
            # runChain(putPuyo(field,next_list[i],candidate["x"],candidate["r"]))
            print(f_list[player][i+1],"フレーム ","次のツモは，",next_list[i+1])
            view_s_field(field[player])
            # 連鎖発生時
            if point[player] - prev_point[player] >= 70:
                print("連鎖発生！ ",math.floor(remaining_point[player]/70),"個のおじゃまを送ります")
                remaining_point[player] = point[player]%70
            print("保有得点 : ",remaining_point[player])
            if i == len(f_list[player])-2:
                print("試合終了")        


if __name__ == "__main__":
    createRecord()

    # print(isX(15279,"1p"))
    # field = [
    #     ['GREEN', 'NULL', 'NULL', 'NULL', 'NULL', 'GREEN'], 
    #     ['GREEN', 'YELLOW', 'NULL', 'NULL', 'NULL', 'GREEN'],
    #      ['YELLOW', 'GREEN', 'PURPLE', 'YELLOW', 'NULL', 'PURPLE'], 
    #      ['YELLOW', 'RED', 'RED', 'PURPLE', 'PURPLE', 'PURPLE'], 
    #      ['RED', 'YELLOW', 'GREEN', 'YELLOW', 'RED', 'PURPLE'],
    #       ['GREEN', 'GREEN', 'YELLOW', 'YELLOW', 'PURPLE', 'GREEN'], 
    #       ['GREEN', 'PURPLE', 'GREEN', 'GREEN', 'YELLOW', 'GREEN'], 
    #       ['RED', 'RED', 'GREEN', 'YELLOW', 'GREEN', 'PURPLE'], ['PURPLE', 'PURPLE', 'RED', 'GREEN', 'PURPLE', 'RED'], ['PURPLE', 'YELLOW', 'GREEN', 'PURPLE', 'YELLOW', 'RED'], ['YELLOW', 'PURPLE', 'GREEN', 'PURPLE', 'RED', 'YELLOW'], ['YELLOW', 'YELLOW', 'PURPLE', 'GREEN', 'GREEN', 'YELLOW'], ['PURPLE', 'PURPLE', 'GREEN', 'RED', 'RED', 'YELLOW']]
    # view_s_field(field)
    # field = runChain(field)
    # view_s_field(field)

# if __name__ == "__main__":
#     img = cv2.imread('./tmp/14545.png')
#     with open('./current.json') as f:
#         area = json.load(f)["area"]

#     print(img2points(img,area))

# view_field(runChain(test3))