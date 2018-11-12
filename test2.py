#フィールドにあるぷよの
sep = {
    "field":{
        "x":6,
        "y":12
    },
    "next":{
        "x":1,
        "y":2
    },
    "wnext":{
        "x":1,
        "y":2
    }
}
for key in sep:
    for i in range(0,sep[key]["y"]):
        for j in range(0,sep[key]["x"]):
            print(i,j)