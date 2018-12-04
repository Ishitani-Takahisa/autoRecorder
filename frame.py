import os
import glob
import cv2
import json
from collections import OrderedDict
from createRecord.createSetting import createSetting

## path2fileName
def getFileName(file):
    return file.lstrip("./movies/").rstrip(".mp4")

createSetting()

files = glob.glob("./movies/*")

for i in range(len(files)):
    fileName = getFileName(files[i])
    path = "./record/"+fileName+".json"

    # print(fileName+"の処理を開始")

    if not os.path.exists(path):
        print(i," : ",fileName)

n = int(input("次に記録した動画の番号を入力してください : "))
cap = cv2.VideoCapture(files[n])
with open("./vs_setting/"+getFileName(files[n])+".json") as f:
    count = json.load(f,object_pairs_hook=OrderedDict)["f_count"]

# TODO : 進捗を表示する https://qiita.com/exy81/items/99e99ab8c184343948cc 参考
for i in range(count):
    _, frame = cap.read()
    cv2.imwrite('./tmp/'+str(i)+'.png',frame)