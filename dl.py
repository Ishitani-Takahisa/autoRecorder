from pytube import YouTube
#import cv2
import os

url = input('>> Prease enter URL : ')
yt = YouTube(url)
print(yt.title)
# ダウンロードしたい形式を選択
video = yt.streams.filter(subtype='mp4').first()
#titleの設定
#video.player_config['args']['title'] = 'out'
# ダウンロード実行
if os.path.isfile('./movies/'+yt.title+'.mp4') :
    print('DL済み')
else:
    print('DL開始')
    video.download('./movies/')
    print('DL完了')
