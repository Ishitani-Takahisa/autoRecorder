import os
import glob
import cv2

## path2fileName
def getFileName(file):
    return file.lstrip("./movies/").rstrip(".mp4")

files = glob.glob("./movies/*")
for file in files:
    fileName = getFileName(file)
    path = "./frames/"+fileName+"/"

    print(fileName+"の処理を開始")

    if not os.path.exists(path):
        os.mkdir(path)

    # print(file)
    # if fileName not in data["separated"]:
    cap = cv2.VideoCapture(file)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite('./frames/'+fileName+'/'+str(i)+'.jpg',frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        i+=1
    cap.release()

    



# cv2.destroyAllWindows()