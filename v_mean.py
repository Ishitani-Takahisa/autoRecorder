import json
import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys

x = []
y = []
z = []
threshold = 150

fig = plt.figure().add_subplot(1,1,1)

def view_progress(start,end,now):
    sys.stdout.write("\r%s" % str(round((1-(end-now)/(end-start))*100,2))+"% \n")

for i in range(12000,16000):
    # if i%100 == 0:
    #     # print(str(round((1-(15600-i)/(15600-10600))*100,2))+"%")
    #     view_progress(11600,15600,i)
    x.append(i)
    y.append(round(cv2.cvtColor(cv2.imread("./tmp/"+str(i)+".png"), cv2.COLOR_BGR2HSV_FULL).T[2].flatten().mean(),2))
    if len(y) >= 2 and ((y[-1] > threshold and y[-2] <= threshold) or (y[-2] > threshold and y[-1] <= threshold)):
        z.append([i,[y[-2],y[-1]]])
    # y.append(i*2)
fig.plot(x, y)
fig.hlines([150], 12000, 16000, linestyles="dashed")
# fig.vlines([12653,12668,14349,14364,15947,15963], 0, 255, linestyles="dashed")
fig.set_xlabel('frame')
fig.set_ylabel('value')
plt.xlim([12000,16000])
plt.ylim([0,255])
plt.show()
# print(z)
plt.savefig('figure.png')
# print(round(cv2.cvtColor(cv2.imread("./tmp/"+str(11163)+".png"), cv2.COLOR_BGR2HSV_FULL).T[2].flatten().mean(),2))