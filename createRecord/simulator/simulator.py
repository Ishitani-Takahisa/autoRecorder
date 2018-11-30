#!/usr/bin/python
# -*- Coding: utf-8 -*-

import sys
test = [
			[0,0,0,0,0,0],
			[0,0,0,0,0,0],
			[0,0,0,0,0,0],
			[0,0,0,0,0,0],
			[0,0,0,0,0,0],
			[0,0,0,0,0,0],
			[0,0,0,0,0,0],
			[0,0,0,0,0,0],
			[0,0,0,0,0,0],
			[0,0,0,0,0,0],
			[0,4,0,3,1,2],
			[3,3,3,1,2,2],
			[4,4,4,3,1,1]
    ]






class pycolor:
    """
    stdoutで用いる色情報保持用クラス
    """
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'


def in3DArray(x,ary):
    """
    3次元配列aryの中に配列xを要素として持つ2次元配列があるかを確認する
    
    Parameters
    ----------
    x : ary
        探す配列x
    ary : ary
        探す元となる配列
    Returns
    -------
    Boolean
        存在したかどうか．
    """
    
    for i in range(len(ary)):
        if x in ary[i]:
            return True
    return False

def copy2DArray(ary):
    """
    二次元配列をシャローコピーする
    
    Parameters
    ----------
    ary : ary
        コピー元の配列
    Returns
    -------
    ary
        コピーした配列
    """
    a = []
    for i in range(len(ary)):
        a.append(ary[i][:])
    return a

class PuyoField():

    field = []
    #x,r,timeを格納した二次配列
    operation_logs = []
    chain_logs = []

    def __init__(self,field,logs):
        self.field = field if field != [] else [[0 for i in range(6)] for j in range(13)]
        self.operation_logs = logs
    
    #test用
    def view_field(self):
        print("---------------")
        for i in range(13):
            sys.stdout.write("| ")
            for j in range(6):
                # sys.stdout.write(str(i)+str(j)+" ")
                puyo = self.field[i][j]
                if puyo is 0:
                    sys.stdout.write("  ")
                elif puyo is 1:
                    sys.stdout.write(pycolor.RED + "● " + pycolor.END)
                elif puyo is 2:
                    sys.stdout.write(pycolor.BLUE + "● " + pycolor.END)
                elif puyo is 3:
                    sys.stdout.write(pycolor.YELLOW + "● " + pycolor.END)
                elif puyo is 4:
                    sys.stdout.write(pycolor.PURPLE + "● " + pycolor.END)

            sys.stdout.write("|\n")
        print("---------------")

    #置ける場所を返す
    def _check_can_put(self,field):
        """
        フィールドを確認し，置ける位置を[x][r]の配列で返す
        
        Parameters
        ----------
        field : ary
            確認する対戦フィールド
        Returns
        -------
        ary
            置けるかどうかを[x][r]でアクセス出来る配列
        """

        #どこに置けるかを示す配列，置けないことが判明したらfalseを与える
        canput = [[True for i in range(4)] for j in range(6)]

        #1番上の段が埋まっているかの確認(縦置き)
        for i in range(6):
            if field[0][i] != 0:
                if i == 0 or i == 5:
                    canput[i][2] = canput[i][0] = False
                if i == 1:
                    canput[i][2] = canput[i][0] = canput[i-1][2] = canput[i-1][0] = False
                if i == 3:
                    canput[i][2] = canput[i][0] = canput[i+1][2] = canput[i+1][0] = canput[i+2][2] = canput[i+2][0] = False
                if i == 4:
                    canput[i][2] = canput[i][0] = canput[i+1][2] = canput[i+1][0] = False
        
        small = -1
        big = 6

        #2(中心)より小さい列と大きい列でそれぞれ12段目が埋まっているか確認する
        #2に近い場所が壁（超えられない）
        for i in range(6):
            if field[1][i] != 0:
                if i < 2:
                    small = small if i < small else i
                else:
                    big = i if i < big else big
        
        #壁を超えるための足がかりとなる11段目が内部にあるか？
        asiba = False
        for i in range(small+1,big):
            if field[2][i] != 0:
                asiba = True

        #足場がない場合は壁を超えられない
        if asiba is False:
            for i in range(6):
                #あとで直す
                if (small != -1 and i <= small) or (big != 6 and big <= i):
                    canput[i][0] = canput[i][2] = False

        for i in range(6):
            #r == 1を考える
            if i < 5 and not canput[i+1][0]:
                canput[i][1] = False
            else:
                canput[i][1] = canput[i][0]
            #r == 3
            if i > 0 and not canput[i-1][0]:
                canput[i][3] = False
            else:
                canput[i][3] = canput[i][0]

        return canput

    #ぷよを落とす
    def _fall_puyo(self,field):
        """
        対戦フィールドを受け取り，浮いているぷよを落としたフィールドを返す
        
        Parameters
        ----------
        field : ary
            対戦フィールド
        Returns
        -------
        ary
            浮いているぷよを落としたフィールド
        """
        f = field[:]
        for i in range(6):
            space = 0
            for j in range(12,-1,-1):
                if f[j][i] is 0:
                    space+=1
                elif space is not 0:
                    f[j+space][i] = f[j][i]
                    f[j][i] = 0
        return f
        
    #ぷよを置く
    def _put_puyo(self,field,tumo,x,r):
        """
        フィールドとツモ，そのツモをどこに置くかを受け取り，置いた後のフィールドを返す
        
        Parameters
        ----------
        field : ary
            対戦フィールド
        tumo : ary
            2個1セットのぷよ
            tumo[0]とtumo[1]に色(int)が入っている
        x : int
            位置 0-5
        r : int
            回転 0-3
            1毎に時計回りに45°回転
        Returns
        -------
        ary
            操作した後のフィールドを返す．
            4連結があっても連鎖を開始する前の状態で返す
        """

        f = field[:]
        if r is 0:
            f = self._fall_puyo(f)
            #2個置けるか確認して置けなかったら下側のみ置く
            if f[1][x] is 0:
                f[0][x] = tumo[0]
                f[1][x] = tumo[1]
            else:
                f[0][x] = tumo[1]
        elif r is 1:
            f = self._fall_puyo(f)
            f[0][x] = tumo[1]
            f[0][x+1] = tumo[0]
        elif r is 2:
            return self._put_puyo(f,tumo[::-1],x,0)
        elif r is 3:
            return self._put_puyo(f,tumo[::-1],x-1,1)
        
        return self._fall_puyo(f)

    #ぷよを消す
    def _vanish_puyo(self,field,chain_list):
        """
        フィールドと4連結している色の位置を受け取って消す
        消した後のフィールドを返すが，落下はさせない．
        
        Parameters
        ----------
        field : ary
            処理を行うフィールド
        chain_list : ary
            4連結以上している位置[i,j]が入った消えるリストの配列の入った配列
            要素数は別々に消える箇所の数
        Returns
        -------
        ary
            処理後のフィールド
        """

        for i in range(len(chain_list)):
            for j in range(len(chain_list[i])):
                field[chain_list[i][j][0]][chain_list[i][j][1]] = 0
        return field               
    
    def _calculate_point(self,f,n,chain_list):
        rensa_bonus = [0, 8, 16, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512]
        renketu_bonus = [0,2,3,4,5,6,7,10]
        color_bonus = [0,3,6,12,24]

        #色と連結数を調べる
        c = []
        ren = []
        count = 0
        for i in range(len(chain_list)):
            #同じ連結内では全て同じ色のため
            if f[chain_list[i][0][0]][chain_list[i][0][1]] not in c:
                c.append(f[chain_list[i][0][0]][chain_list[i][0][1]])
            ren.append(len(chain_list[i])-4)
            count += len(chain_list[i])
        
        #連結ボーナスはループを回す必要があるので予め出す
        ren_b = 0
        for i in range(len(ren)):
            if ren_b < 7:
                ren_b += renketu_bonus[ren[i]]
            else:
                ren_b +=10

        bonus = color_bonus[len(c)-1]+rensa_bonus[n]+ren_b if color_bonus[len(c)-1]+rensa_bonus[n]+ren_b > 0 else 1
        return count*10*bonus

    #連結を数える
    def _count_link(self,i,j,f,link):
        c = f[i][j]
        f[i][j] = -1
        link.append([i,j])
        if j > 0 and f[i][j-1] is c:
            self._count_link(i,j-1,f,link)
        if j < 5 and f[i][j+1] is c:
            self._count_link(i,j+1,f,link)
        if i > 1 and f[i-1][j] is c:
            self._count_link(i-1,j,f,link)
        if i < 12 and f[i+1][j] is c:
            self._count_link(i+1,j,f,link) 
        return link

    #すべての連結を確認する
    def _count_all_link(self,f):
        link = []
        for i in range(13):
            for j in range(6):
                #お邪魔ぷよではなく，連結未確認
                if f[i][j] is not 0 and not in3DArray([i,j],link):
                    link.append(self._count_link(i,j,copy2DArray(f),[]))
        return link

    #連鎖が発生したか確認する．発生してたら消える連結のリストを返す
    def _check_occur_chain(self,f):
        link = self._count_all_link(f)
        chain_list = []
        # print(link)
        for i in range(len(link)):
            if len(link[i]) >= 4:
                chain_list.append(copy2DArray(link[i]))
        return chain_list     

    def record_chain(self,field):
        f = copy2DArray(field)
        c_list = self._check_occur_chain(f)
        n = 0
        point = 0
        while(c_list != []):
            n+=1
            point += self._calculate_point(f,n,c_list)
            f = self._fall_puyo(self._vanish_puyo(f,c_list))
            c_list = self._check_occur_chain(f)
        
        self.chain_logs.append({
            "i" : len(self.operation_logs),
            "n" : n,
            "point":point
        })
        return f

    #画像認識で得られた盤面からどの操作をしたか特定する
    def reverce_operate(self,f,nf,tumo):
        pass

    #操作の大元
    def operate(self,tumo,x,r,time):
        #きちんと置ける場合
        if self._check_can_put(self.field)[x][r]:
            self.operation_logs.append({
                "x":x,
                "r":r,
                "time":time
            })
            self.field = self._put_puyo(self.field,tumo,x,r)
            # self.view_field()
            chain_list = self._check_occur_chain(self.field)
            if chain_list != []:
                print("連鎖発生")
                self.field = self.record_chain(self.field)
                print(self.chain_logs)
                # self.view_field()
        else:
            #error
            print("e?")
            # self.view_field()
            print(self._check_can_put(self.field),x,r)




class PuyoSim():
    
    """
    ぷよぷよに関する全ての情報を1試合分持つクラス
    イニシャライザは存在しない

    Attributes
    ----------
    _1p : puyoField
        1pに関する情報
    _2p : puyoField
        2pに関する情報
    _tumo : ary
        ツモ情報を入れる2次元配列
        ツモ情報は色(int)の要素が2つある配列     
    """

    
    _1p = PuyoField(test,[])
    _2p = PuyoField([],[])
    _tumo = []
    
    def add_tumo(self,tumo):
        """
        ツモを1セット受け取って追加する
        
        
        Parameters
        ----------
        tumo : ary
            色(int)が入った要素が2個の配列
        
        """

        self._tumo.append(tumo)

    def operate(self,player,x,r,time):
        # self.add_tumo()
        if player == 1:
            #置くぷよはツモの操作回数目にある
            self._1p.operate(self._tumo[len(self._1p.operation_logs)],x,r,time)
        else:
            self._2p.operate(self._tumo[len(self._1p.operation_logs)],x,r,time)

    def test(self):
        print(self._1p.field)
    
sim = PuyoSim()
sim.add_tumo([1,3])
sim.add_tumo([2,4])
sim.operate(1,1,1,3)
sim.operate(1,4,1,4)
# sim.test()