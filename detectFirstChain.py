import cv2
from createRecord.img2points import patternMatch

def detectFirstChain(start,end,area,player):
    template = cv2.imread("./images/x.png",0)
    for i in range(start,end):
        match_list = patternMatch(cv2.cvtColor(cv2.imread("./tmp/"+str(i)+".png"), cv2.COLOR_BGR2GRAY)[area["top"]:area["top"]+area["height"],area[player]:area[player]+area["width"]],template)
        if len(match_list) != 0:
            return i
# area = {"top": 615, "width": 300, "height": 60, "1p": 193}
# print(detectFirstChain(15638,15639,area,"1p"))