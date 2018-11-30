import os
import glob
import cv2
import json
from collections import OrderedDict

def createSetting():
    ## path2fileName
    def getFileName(file):
        return file.lstrip("./movies/").rstrip(".mp4")

    files = glob.glob("./movies/*")

    files = glob.glob("./movies/*")
    for file in files:
        fileName = getFileName(file)
        path = "./vs_setting/"+fileName+".json"

        if not os.path.exists(path):
            cap = cv2.VideoCapture(file)
            with open('./vs_setting/'+fileName+".json",'w') as f:
                json.dump({
                    "title" : fileName,
                    "fps" : int(cap.get(cv2.CAP_PROP_FPS)),
                    "f_count" : int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                },f,ensure_ascii=False)