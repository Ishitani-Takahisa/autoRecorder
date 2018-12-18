import json
import cv2
# from createRecord.detectNextChange import detectNextChange

with open("./current.json") as f:
    current = json.load(f)
    area = current["area"]

# # [14364, [117.41, 151.57]], [15947, [196.04, 125.43]]
# print(detectNextChange(14364,15947))

from createRecord.img2points import img2points

print(img2points(cv2.imread("./tmp/15343.png"),area),)