#!/usr/bin/python
# -*- Coding: utf-8 -*-

import sys
import os
from pynput.keyboard import Key, Listener
from simulator import PuyoField,pycolor,in3DArray,copy2DArray

from pynput.keyboard import Key, Listener

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


def view_operate_puyo(x,r,puyo):
    pass
    

def view_field(field,next):
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

class PlayField(PuyoField):
    def __init__(self,field,logs):
        self.field = field if field != [] else [[0 for i in range(6)] for j in range(13)]
        self.operation_logs = logs

class PlaySim():
    _p = PlayField([],[])
    _tumo = [[1,3],[2,4],[2,2]]

    def add_tumos(self,*tumos):
        for tumo in tumos:
            self._tumo.append(tumo)
    
    def add_rand_tumos(self):
        pass

    def operate(self,x,r):
        self._p.operate(self._tumo[len(self._p.operation_logs)],x,r,0)

sim = PlaySim()
sim.add_tumos([1,3],[2,4],[2,2])
sim.operate(1,1)
sim.operate(4,1)

def on_press(key):

    if key == Key.esc:
        sys.exit()

    try:
        os.system('clear')
        # view_field(sim._p.field,[[1,2],[1,1]])
        print(key.char)

    except AttributeError:
        os.system('clear')
        print(key)

        view_field(sim._p.field,[[1,2],[1,1]])

if __name__ == '__main__':

    with Listener(
        on_press = on_press,
    ) as listener:
        listener.join()
