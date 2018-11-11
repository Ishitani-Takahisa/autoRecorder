import numpy as np
import cv2

##BGR
a = np.uint8([[[250,180,55]]])
aa = cv2.cvtColor(a,cv2.COLOR_BGR2HSV)
print(aa)