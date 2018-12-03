# -*- coding: utf-8 -*-
import cv2
import json

#自作
from createRecord.img2points import img2points

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
    #最後の試合か確認する
    if f_count - start < fps+1:
        return 0
    for i in range(10,fps+1,10):
        print("終了条件を確認しています",i,"/",fps)
        check = img2points(cv2.imread('./tmp/'+str(start+i)+'.png'),area)
        if check[0] != -1 and check[0] != -1:
            break
        elif i == fps:
            return 0
    
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
            return detect(i-round(interval/2),round(interval/2),point)

        p = img2points(cv2.imread('./tmp/'+str(i)+'.png'),area)

        #test
        # if i > 11908:
        #     print(p[0],point)

        #試合が終了していたらそこで終わる
        if p[0] == -1 and p[1] == -1:
            for j in range(abs(interval)):
                p = img2points(cv2.imread('./tmp/'+str(i-j)+'.png'),area)
                if p[0] != -1 and p[1] != -1:
                    return i-j
        #連鎖中だったら0.3秒進める
        if p[0] < 0:
            return detect(i+round(0.3*fps),interval,point)
        
        if p[0] == 0 and abs(interval) == 1:
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
    
    return detect(start,30*fps,0)
    

# with open("./vs_setting/ぷよぷよクロニクル 第2回おいうリーグ S級リーグ ようかん vs まはーら 50先.json") as f:
#     setting = json.load(f)

# with open('./test/area.json') as f:
#     area = json.load(f)
#     print(detectOneGame(setting,area,162960))

