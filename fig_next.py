import json
import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
from createRecord.isPuyoColor import next2array

def detectNextChange(start,end,area):
    """開始と終了のフレーム数を与えて，ネクストが切り替わったフレームを返す
    
    Parameters
    ----------
    df : array
        {
            start : int(開始フレーム数)
            end : int(終了フレーム)
            area : dict
                nextの入ったdict
                {
                    "top":基準となる座標 i,
                    "1p":基準となる座標 j,
                    "2p":基準となる座標 j,
                    "height:範囲の高さ,
                    "width":範囲の幅
                }
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
    
    x = []
    y = []
    y2 = []
    y3 = []

    df = []
    for i in range(start,end):
        p,_ = next2array(cv2.imread('./tmp/'+str(i)+'.png'),area)
        df.append(p)
        # start
        x.append(i)
        # end

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
                        # ここから
                        # 記録は1pのみ
                        if p == "1p":
                            y.append(0)
                            y2.append(0)
                            y3.append(0)
                        # ここまで                        
                        continue
                    else:
                        count_diff = 0
                        for x in diff:
                            count_diff+=x["diff"]
                        # ここから
                        # 記録は1pのみ
                        if p == "1p":
                            y.append(count_diff)
                        # ここまで
                        if count_diff > 2:
                            "２重チェック"
                            if i < len(df)-1:
                                # print(i,len(df))
                                diff2 = find_diff(df[i-1][p][j],df[i+1][p][j])
                                count_diff2 = 0
                                for x in diff2:
                                    count_diff2+=x["diff"]
                                # ここから
                                # 記録は1pのみ
                                if p == "1p":
                                    y2.append(count_diff2)
                                # ここまで
                                if count_diff2 < 30:
                                    if p == "1p":
                                        y3.append(0)
                                    continue
                                else:
                                    if p == "1p":
                                        y3.append(count_diff)
                            #     print(i,count_diff," diff2 ",diff2)
                            # print(i," diff ",diff)
                            # if cv2.cvtColor(cv2.imread("./tmp/"+str(i)+".png"), cv2.COLOR_BGR2HSV_FULL).T[2].flatten().mean() > 150:
                            players[p].append(start+i)
                        else:
                            # ここから
                            # 記録は1pのみ
                            if p == "1p":
                                y2.append(0)
                                y3.append(0)
                            # ここまで
                else:
                    y.append(0)
                    y2.append(0)
                    y3.append(0)
    

    # figure
    # subplot(2,2,1)        % add first plot in 2 x 2 grid
    # plot(x,y1)            % line plot

    # subplot(2,2,2)        % add second plot in 2 x 2 grid
    # scatter(x,y2)         % scatter plot

    # subplot(2,2,[3 4])    % add third plot to span positions 3 and 4
    # yyaxis left           % plot against left y-axis 
    # plot(x,y1)           
    # yyaxis right          % plot against right y-axis
    # plot(x,y2)
    fig = plt.figure().add_subplot(1,1,1)
    print(len(x),len(y))
    fig.plot(x, y)
    # fig.plot(x, y2)
    # fig.plot(x, y3)
    fig.set_xlabel('frame')
    fig.set_ylabel('diff')
    plt.xlim([12668,14349])
    # plt.ylim([0,255])
    plt.show()
    # plt.savefig('figure.png')
    
    return players
    


next = {"top": 93, "width": 50, "height": 90, "1p": 533, "2p": 703}
print(detectNextChange(12668,14349,next))
