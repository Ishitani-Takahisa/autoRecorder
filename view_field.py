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

def view_field(field,next):
    """フィールドを出力する
    
    Parameters
    ----------
    field : [13][6]
        ぷよぷよのフィールド
    next : function
        [description]
    
    """


    sys.stdout.write(pycolor.CYAN + "---------------   -----\n" + pycolor.END)
    for i in range(13):
        sys.stdout.write(pycolor.CYAN +"| " + pycolor.END)
        for j in range(6):
            write_puyo(field[i][j])

        if i is 0 or i is 1:
            sys.stdout.write(pycolor.CYAN + "|   | "+ pycolor.END)
            write_puyo(next[0][i])
            sys.stdout.write(pycolor.CYAN +"|\n"+ pycolor.END)
        elif i is 2:
            sys.stdout.write(pycolor.CYAN + "|    \ "+ pycolor.END)
            write_puyo(next[1][0])
            sys.stdout.write(pycolor.CYAN +"\ \n"+ pycolor.END)
        elif i is 3:
            sys.stdout.write(pycolor.CYAN + "|    | "+ pycolor.END)
            write_puyo(next[1][1])
            sys.stdout.write(pycolor.CYAN +"|\n"+ pycolor.END)
        elif i is 4:
            sys.stdout.write(pycolor.CYAN + "|    -----\n"+ pycolor.END)
        else:
            sys.stdout.write(pycolor.CYAN + "|\n" + pycolor.END)
    sys.stdout.write(pycolor.CYAN + "---------------\n" + pycolor.END)


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
if __name__ == "__main__":
    view_field(test,[[1,1],[1,2]])