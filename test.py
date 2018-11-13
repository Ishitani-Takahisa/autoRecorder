import numpy as np
import cv2

##BGR
a = np.uint8([[[34,30,203]]])
aa = cv2.cvtColor(a,cv2.COLOR_BGR2HSV)
print(aa)


while True:
    print("R")
    red = input('>>>  ')
    print("G")
    green = input('>>>  ')
    print("B")
    blue = input('>>>  ')
    print(cv2.cvtColor(np.uint8([[[blue,green,red]]]),cv2.COLOR_BGR2HSV))