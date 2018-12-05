import numpy as np
import cv2
from matplotlib import pyplot as plt

plt.gray()
# img = cv2.imread("./test/sample.jpg")
img = cv2.imread("./tmp/10196.png")
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# 2hsv
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

l = [0 for i in range(3)]
u = [255 for i in range(3)]
lower = np.array([0,0,210])
upper = np.array([250,60,255])
text = ["H","S","V"]

# TODO : BLUEの修正
while True:
    command = input("どちらを変更しますか l/u？")
    if command == ("l" or "L"):
        print("下限を変更します")
        for i in range(3):
            l[i] = int(input(text[i] + "の入力をお願いします"))
        print("下限を",l,"に設定します")
        lower = np.array(l)
    elif command == ("u" or "U"):
        print("上限を変更します")
        for i in range(3):
            u[i] = int(input(text[i] + "の入力をお願いします"))
        print("上限を",u,"に設定します")
        upper = np.array(u)
    elif command == "u1":
        print("H上限のみ変更します")
        u[0] = int(input("入力をお願いします"))
        print("上限を",u,"に設定します")
        upper = np.array(u)
    elif command == "c":
        print("RGBをHSVに変換します")
        print("R")
        red = input('>>>  ')
        print("G")
        green = input('>>>  ')
        print("B")
        blue = input('>>>  ')
        print(cv2.cvtColor(np.uint8([[[blue,green,red]]]),cv2.COLOR_BGR2HSV))
        continue
    elif command == "v":
        pass
    else:
        print("誤った入力です")
        continue
    
    img_mask = cv2.inRange(hsv_img, lower, upper)
    plt.imshow(img_mask)
    plt.show()



