#!/usr/bin/python
# -*- Coding: utf-8 -*-

import sys
import math

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

def write_puyo(puyo):
    if puyo is "NULL":
        sys.stdout.write("  ")
    elif puyo is "RED":
        sys.stdout.write(pycolor.RED + "● " + pycolor.END)
    elif puyo is "BLUE":
        sys.stdout.write(pycolor.BLUE + "● " + pycolor.END)
    elif puyo is "YELLOW":
        sys.stdout.write(pycolor.YELLOW + "● " + pycolor.END)
    elif puyo is "GREEN":
        sys.stdout.write(pycolor.GREEN + "● " + pycolor.END)
    elif puyo is "PURPLE":
        sys.stdout.write(pycolor.PURPLE + "● " + pycolor.END)
    elif puyo is "OJAMA":
        sys.stdout.write("● ")

def viewField(field):
    """フィールドを出力する
    
    Parameters
    ----------
    field : dict
        {
            "field":{
                "1p":[y][x]にkeyとなるcolorのstr,
                "2p"
            },
            "next":{},
            "wnext":{}
        }

    """


    sys.stdout.write(pycolor.CYAN + "---------------   -----     -----   ---------------\n" + pycolor.END)
    for i in range(12):
        sys.stdout.write(pycolor.CYAN +"| " + pycolor.END)
        for j in range(6):
            write_puyo(field["field"]["1p"][i][j])

        if i is 0 or i is 1:
            sys.stdout.write(pycolor.CYAN + "|   | "+ pycolor.END)
            write_puyo(field["next"]["1p"][0][i])
            sys.stdout.write(pycolor.CYAN +"|     | ")
            #2p
            write_puyo(field["next"]["2p"][0][i])
            sys.stdout.write(pycolor.CYAN +"|   | ")
            for j in range(6):
                write_puyo(field["field"]["2p"][i][j])
            sys.stdout.write(pycolor.CYAN +"| ")
            sys.stdout.write("\n"+ pycolor.END)
        elif i is 2:
            sys.stdout.write(pycolor.CYAN + "|    \ "+ pycolor.END)
            write_puyo(field["next"]["1p"][1][0])
            sys.stdout.write(pycolor.CYAN +"\   / ")
            #2p
            write_puyo(field["next"]["2p"][1][0])
            sys.stdout.write(pycolor.CYAN + "/    | ")
            for j in range(6):
                write_puyo(field["field"]["2p"][i][j])
            sys.stdout.write("|\n"+ pycolor.END)
        elif i is 3:
            sys.stdout.write(pycolor.CYAN + "|    | "+ pycolor.END)
            write_puyo(field["next"]["1p"][1][1])
            sys.stdout.write(pycolor.CYAN +"|   | ")
            #2p
            write_puyo(field["next"]["2p"][1][1])
            sys.stdout.write(pycolor.CYAN +"|    | "+ pycolor.END)
            for j in range(6):
                write_puyo(field["field"]["2p"][i][j])
            sys.stdout.write(pycolor.CYAN +"|\n"+ pycolor.END)
        elif i is 4:
            sys.stdout.write(pycolor.CYAN + "|    -----   -----    | "+ pycolor.END)
            for j in range(6):
                write_puyo(field["field"]["2p"][i][j])
            sys.stdout.write(pycolor.CYAN +"|\n"+ pycolor.END)
        else:
            sys.stdout.write(pycolor.CYAN +"|                     | "+ pycolor.END)
            for j in range(6):
                write_puyo(field["field"]["2p"][i][j])
            sys.stdout.write(pycolor.CYAN + "|\n" + pycolor.END)
    sys.stdout.write(pycolor.CYAN + "---------------                     ---------------\n" + pycolor.END)


def viewPoint(p1,p2):
    d1 =14 if p1<0 else 15-int (math.log10(p1) + 1) if p1 != 0 else 14
    d2 =14 if p2<0 else 15-int (math.log10(p2) + 1) if p2 != 0 else 14
    # print(d1," ",d2)
    sys.stdout.write(" "*int(d1/2)+(str(p1) if p1 > 0 else "x")+" "*(d1-int(d1/2))+"                     "+" "*int(d2/2)+(str(p2) if p2 > 0 else "x")+" "*(d2-int(d2/2))+"\n")

def viewAll(field,point):
    """フィールド及びネクストの配列の入ったdictと1p,2pのポイントが入った配列を受け取って表示する
    
    Parameters
    ----------
    field : dict
        {
            "1p": {
                "field":[12][6]
                "next":[2][2]
            },
            "2p":{}
            
        }
    point : array[int]
        [1p,2p]
    
    """

    viewField(field)
    viewPoint(point[0],point[1])

if __name__ == "__main__":
    test = [
        ["NULL","NULL","NULL","NULL","NULL","NULL"],
        ["NULL","NULL","NULL","NULL","NULL","NULL"],
        ["NULL","NULL","NULL","NULL","NULL","NULL"],
        ["NULL","NULL","NULL","NULL","NULL","NULL"],
        ["NULL","NULL","NULL","NULL","NULL","NULL"],
        ["NULL","NULL","NULL","NULL","NULL","NULL"],
        ["NULL","NULL","NULL","NULL","NULL","NULL"],
        ["NULL","NULL","NULL","NULL","NULL","NULL"],
        ["NULL","NULL","NULL","NULL","NULL","NULL"],
        ["NULL","YELLOW","NULL","GREEN","RED","BLUE"],
        ["GREEN","GREEN","GREEN","RED","BLUE","BLUE"],
        ["YELLOW","YELLOW","YELLOW","GREEN","RED","RED"]
    ]
    viewAll({
        "field":{
            "1p":test,
            "2p":test
        },
        "next": {
            "1p":[["RED","RED"],["YELLOW","GREEN"]],
            "2p":[["RED","RED"],["YELLOW","GREEN"]]
        },
        "wnext": {
            "1p":[["RED","RED"],["YELLOW","GREEN"]],
            "2p":[["RED","RED"],["YELLOW","GREEN"]]
        }
    },[100000,50])