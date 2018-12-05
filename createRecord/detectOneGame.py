# -*- coding: utf-8 -*-
import cv2
import json
import math

#自作
from createRecord.img2points import img2points

def first_bright(start,end,interval):
    def detect(i,interval):
        # print(i,cv2.cvtColor(cv2.imread("./tmp/"+str(i)+".png"), cv2.COLOR_BGR2HSV_FULL).T[2].flatten().mean())
        if end < i:
            return detect(math.ceil((end+i)/2),end-i)
        elif end == i:
            #start返すのも面白いかも
            return i
        if cv2.cvtColor(cv2.imread("./tmp/"+str(i)+".png"), cv2.COLOR_BGR2HSV_FULL).T[2].flatten().mean() < 150:
             return detect(i+interval,interval)
        elif interval == 1:
            return i
        else:
            return detect(i-round(interval*3/2),round(interval/2))
    
    return detect(start,interval)
        

def detectOneGame(setting,area,start):
    """試合の終わり（次の試合の始まりを探す）
    
    Parameters
    ----------
    setting : dict
        createSettingで作ったやつ
        ./vs_setting/title.json
    area : dict
        そのまま
    start : int
        試合開始フレーム
    
    Returns
    -------
    int
        終了フレーム
    """

    fps = setting["fps"]
    f_count = setting["f_count"]
    s = first_bright(start,f_count,int(fps/15))    
    def detect(i,interval,point):
        """実際に見つける再帰関数
        
        Parameters
        ----------
        i : int
            今のフレーム
        interval : int
            探す間隔
        
        Returns
        -------
        i
            見つかったフレーム
        """

        #test
        # if i > 11908:
        #     print(i,interval,point)

        #ファイルが存在する範囲でのみ調べる
        if f_count < i:
            if interval == 1:
                return f_count 
            return detect(i-round(interval/2),round(interval/2),point)
            # return detect(math.ceil((f_count+i)/2),f_count-i,point)
            # return detect(i,1,point)


        p = img2points(cv2.imread('./tmp/'+str(i)+'.png'),area)

        #test
        # if i > 11908:
        #     print(p[0],point)

        #試合が終了していたらそこで終わる
        if p[0] == -1 or p[1] == -1:
            return first_bright(i,f_count,int(fps/15))
            # p = img2points(cv2.imread('./tmp/'+str(end)+'.png'),area)
            # if p[0] == 0 or p[1] == 0:
            #     return end

        #連鎖中だったら0.3秒進める
        if p[0] < 0:
            if i + round(0.3*fps) > f_count:
                return f_count
            return detect(i+round(0.3*fps),interval,point)
        
        if p[0] == 0 and p[1] == 0 and abs(interval) == 1:
            return i
        elif point <= p[0]:
            #減ってから増やす場合は，増量を半減する
            if interval > 0:
                return detect(i+interval,interval,p[0])
            else:
                return detect(i-round(interval/2),-1*round(interval/2),p[0])
        elif p[0] < point:
            #減らした後同じ数増やさないように符号で示す
            interval = -1*round(interval/2) if interval > 0 else round(interval/2)
            return detect(i+interval,interval,point)
    
    return detect(s,30*fps,0)
    

# with open("./vs_setting/ぷよぷよクロニクル 第2回おいうリーグ S級リーグ ようかん vs まはーら 50先.json") as f:
#     setting = json.load(f)

# with open('./area.json') as f:
#     area = json.load(f)
#     print(detectOneGame(setting,area,145343))

