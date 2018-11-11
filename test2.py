def width2field(top,left,right,player):
    def kiriyoku(n,m):
        return n if n%m==0 else n+(m-n%m) if n%m>m/2 else n-n%m

    pf = {
        "left":left,
        "right":right,
    }
    while (pf["right"] - pf["left"]) % 6 != 0:
        pf["left"]+=1
        if (pf["right"] - pf["left"]) % 6 > 0:
            pf["right"]-=1

    width = pf["right"] - pf["left"]

    # h = round(width*1.8)
    # height = h if h%12==0 else h+(12-h%12) if h%12>5 else h-h%12
    height = kiriyoku(round(width*1.8),12)

    player_1_left = pf["left"] if player == 1 else pf["left"]-2*width

    return {
        "field":{
            "top":top,
            "width":width,
            "height":height,
            "1p":player_1_left,
            "2p":player_1_left+2*width
        },
        "next": {
            "top":top+round(width/15),
            "width":round(width/6),
            "height":kiriyoku(round(width*0.3),2),
            "1p":player_1_left+width+round(width*2/15),
            "2p":player_1_left+2*width-round(width*2/15)-round(width/6)
        }
    }


t = 156
l = 27
r = 682
print(width2field(t,l,r,1))