def countWhite(img,start,end):
    #count white
    dictX = {}
    dictY = {}
    shape = img.shape
    for i in range(start["y"],end["y"]):
        for j in range(start["x"],end["x"]):
            if img[i,j] == 255:
                if str(i) not in dictX:
                    dictX[str(i)] = 1
                else:
                    dictX[str(i)] += 1
                if str(j) not in dictY:
                    dictY[str(j)] = 1
                else:
                    dictY[str(j)] += 1
    return {
        "x" : dictX,
        "y" : dictY
    }