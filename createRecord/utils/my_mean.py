#meanに不具合があるため．自分でmeanを作る
def myMean(arr):
    n = 0
    total = 0.0
    for x in arr:
        total += x
        n += 1
    return total / n