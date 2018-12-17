import cv2
import json
from createRecord.isPuyoColor import next2array
with open("./current.json") as f:
    current = json.load(f)
area = current["area"]["next"]
def frame2next(frame):
    p,p2 = next2array(cv2.imread('./tmp/'+str(frame)+'.png'),area)
    return p2

def detectNextColor(f_list,player):
    nextlist = []
    for f in f_list:
        next = frame2next(f-3)[player]
        # if len(nextlist) != 0 and nextlist[-1] == next:
        #     print(f,"連続")
        nextlist.append(next)
    return nextlist
    # print(f,next)
    # if 'NULL' in next:
    #     print(f-3,next)
    #     p,p2 = next2array(cv2.imread('./tmp/'+str(f)+'.png'),area)
    #     print(p["1p"])

if __name__ == "__main__":
    f_original = [14365, 14440, 14464, 14491, 14517, 14542, 14572, 14597, 14623, 14647, 14687, 14714, 14747, 14771, 14795, 14842, 14874, 14894, 14917, 14939, 14960, 14983, 15014, 15034, 15053, 15072, 15093, 15125, 15153, 15191, 15209, 15227, 15244, 15262, 15279, 15654, 15725, 15753, 15776, 15947, 15962]
    f_list = [14440, 14464, 14491, 14517, 14542, 14572, 14597, 14623, 14647, 14687, 14714, 14747, 14771, 14795, 14842, 14874, 14894, 14917, 14939, 14960, 14983, 15014, 15034, 15053, 15072, 15093, 15125, 15153, 15191, 15209, 15227, 15244, 15262, 15279, 15725, 15753, 15776, 15947]
    