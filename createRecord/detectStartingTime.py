# -*- coding: utf-8 -*-
import cv2
import json

#自作
from createRecord.img2points import patternMatch

with open("./vs_setting/ぷよぷよクロニクル 第２回おいうリーグ S級リーグ まはーら vs makkyu 50先 実況枠.json") as f:
    setting = json.load(f)

def detectStartingTime(fps):
    """設定を読み込んで試合開始時間を探す
    
    Parameters
    ----------
    fps : int
        ./vssetting.動画タイトル.json["fps"]
    
    Returns
    -------
    int
        試合が開始するフレーム,最初に見つけたフレームの0.3s == 0.3*fps後を返している．
        最初のフレームでは，ネクストやエリアが正しく取れないため．
    """

    def detect(i,interval):
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
        if len(patternMatch(cv2.cvtColor(cv2.imread('./tmp/'+str(i)+'.png'), cv2.COLOR_BGR2GRAY),cv2.imread('./images/star.png',0))) == 0:
            return detect(i+interval,interval)
        elif interval == 1:
            return i
        else:
            interval = round(interval/2)
            return detect(i-interval,interval)

    interval = fps*60
    return detect(0,interval) + int(0.3*fps)

def detectEndTime(fps,f_count):
    """設定を読み込んで試合開始時間を探す
    
    Parameters
    ----------
    fps : int
        ./vssetting.動画タイトル.json["fps"]
    f_count : int
        ./vssetting.動画タイトル.json["f_count"]
    
    Returns
    -------
    int
        試合が終了するフレーム,後ろから探して最初に見つけたフレームを返している．
    """

    def detect(i,interval):
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
        if len(patternMatch(cv2.cvtColor(cv2.imread('./tmp/'+str(i)+'.png'), cv2.COLOR_BGR2GRAY),cv2.imread('./images/star.png',0))) == 0:
            return detect(i-interval,interval)
        elif interval == 1:
            return i
        else:
            interval = round(interval/2)
            return detect(i+interval,interval)

    interval = fps*10
    return detect(f_count-interval,interval)

# print(detectStartingTime(setting["fps"]))
# print(detectEndTime(setting["fps"],setting["f_count"]-1))