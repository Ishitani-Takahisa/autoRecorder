import cv2
from createRecord.isPuyoColor import next2array

def detectNextChange(start,end,area):
    """開始と終了のフレーム数を与えて，ネクストが切り替わったフレームを返す
    
    Parameters
    ----------
    df : array
        {
            start : int(開始フレーム数)
            next_list : [{
                1p : next == [2][2],
                2p :
            }]
        }
    
    Returns
    -------
    players : {'1p': [10504, 10532], '2p': [10505, 10528]}
        key : 1p,2p
        value : 変化のあったフレーム数
    """

    def find_diff(a1,a2):
        """２つのぷよの確率の入った配列が同等か確認し，差がある場合は，どの程度違うのかintで返す．
        
        Parameters
        ----------
        a1,a2 : dict  
            key == color
        
        Returns
        -------
        df : array
            [{
                key : "異なったcolor",
                diff : "異なった量"
            }]
        """

        df = []
        if a1 == a2:
            return df
        for key in a1:
            if a1[key] != a2[key]:
                df.append({
                    "key":key,
                    "diff":abs(a1[key]-a2[key])
                })
        return df
    
    df = []
    for i in range(start,end):
        p,_ = next2array(cv2.imread('./tmp/'+str(i)+'.png'),area)
        df.append(p)

    players = {
        "1p":[],
        "2p":[]
        }

    for i,x in enumerate(df):
        for j in range(2):
            for p in players:
                if i != 0 and (len(players[p]) == 0 or players[p][-1]+7 <= start+i):
                    diff = find_diff(df[i][p][j],df[i-1][p][j])
                    if len(diff) == 0:
                        continue
                    else:
                        count_diff = 0
                        for x in diff:
                            count_diff+=x["diff"]
                        if count_diff > 2:
                            "２重チェック"
                            if i != end:
                                diff2 = find_diff(df[i-1][p][j],df[i+1][p][j])
                                for x in diff2:
                                    count_diff+=x["diff"]
                                if count_diff < 5:
                                    continue
                            players[p].append(start+i)
    
    return players



# print(findNextChange(7115,8671,area["next"]))
    