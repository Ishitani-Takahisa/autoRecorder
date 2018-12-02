#!/usr/bin/python
# -*- Coding: utf-8 -*-

import sys

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

def view_field(field,next):
    """フィールドを出力する
    
    Parameters
    ----------
    field : [2][13][6]
        ぷよぷよのフィールド
        [2]はプレイヤー
    next : [2][2][2]
        player - next&wnext - tumo
    
    """


    sys.stdout.write(pycolor.CYAN + "---------------   -----     -----   ---------------\n" + pycolor.END)
    for i in range(13):
        sys.stdout.write(pycolor.CYAN +"| " + pycolor.END)
        for j in range(6):
            write_puyo(field[0][i][j])

        if i is 0 or i is 1:
            sys.stdout.write(pycolor.CYAN + "|   | "+ pycolor.END)
            write_puyo(next[0][0][i])
            sys.stdout.write(pycolor.CYAN +"|     | ")
            #2p
            write_puyo(next[1][0][i])
            sys.stdout.write(pycolor.CYAN +"|   | ")
            for j in range(6):
                write_puyo(field[1][i][j])
            sys.stdout.write(pycolor.CYAN +"| ")
            sys.stdout.write("\n"+ pycolor.END)
        elif i is 2:
            sys.stdout.write(pycolor.CYAN + "|    \ "+ pycolor.END)
            write_puyo(next[0][1][0])
            sys.stdout.write(pycolor.CYAN +"\   / ")
            #2p
            write_puyo(next[1][1][0])
            sys.stdout.write(pycolor.CYAN + "/    | ")
            for j in range(6):
                write_puyo(field[1][i][j])
            sys.stdout.write("|\n"+ pycolor.END)
        elif i is 3:
            sys.stdout.write(pycolor.CYAN + "|    | "+ pycolor.END)
            write_puyo(next[0][1][1])
            sys.stdout.write(pycolor.CYAN +"|   | ")
            #2p
            write_puyo(next[1][1][1])
            sys.stdout.write(pycolor.CYAN +"|    | "+ pycolor.END)
            for j in range(6):
                write_puyo(field[1][i][j])
            sys.stdout.write(pycolor.CYAN +"|\n"+ pycolor.END)
        elif i is 4:
            sys.stdout.write(pycolor.CYAN + "|    -----   -----    | "+ pycolor.END)
            for j in range(6):
                write_puyo(field[1][i][j])
            sys.stdout.write(pycolor.CYAN +"|\n"+ pycolor.END)
        else:
            sys.stdout.write(pycolor.CYAN +"|                     | "+ pycolor.END)
            for j in range(6):
                write_puyo(field[1][i][j])
            sys.stdout.write(pycolor.CYAN + "|\n" + pycolor.END)
    sys.stdout.write(pycolor.CYAN + "---------------                     ---------------\n" + pycolor.END)


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
    ["NULL","NULL","NULL","NULL","NULL","NULL"],
    ["NULL","YELLOW","NULL","GREEN","RED","BLUE"],
    ["GREEN","GREEN","GREEN","RED","BLUE","BLUE"],
    ["YELLOW","YELLOW","YELLOW","GREEN","RED","RED"]
]
if __name__ == "__main__":
    view_field([test,test],[[["RED","RED"],["YELLOW","GREEN"]],[["GREEN","GREEN"],["BLUE","GREEN"]]])