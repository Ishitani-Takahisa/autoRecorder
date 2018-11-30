import sys
import os
import curses

class pycolor:
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

field = [
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

field = [
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
			[0,2,0,0,0,0],
			[0,4,1,0,0,0],
			[4,4,4,0,0,0]
    ]


def view_field(field):
    sys.stdout.write(pycolor.CYAN + "---------------\n" + pycolor.END)
    for i in range(13):
        sys.stdout.write(pycolor.CYAN +"| " + pycolor.END)
        for j in range(6):
            puyo = field[i][j]
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

        sys.stdout.write(pycolor.CYAN + "|"+str(i)+"\n" + pycolor.END)
    sys.stdout.write(pycolor.CYAN + "---------------\n" + pycolor.END)
# os.system('clear')


# 00 01 02... 05 
# 120 121... 125

#f is field
#n is count of link

def in3DArray(x,ary):
    for i in range(len(ary)):
        if x in ary[i]:
            return True
    return False



def copy2DArray(ary):
    a = []
    for i in range(len(ary)):
        a.append(ary[i][:])
    return a



def count_link(i,j,f,link):
    c = f[i][j]
    f[i][j] = -1
    link.append([i,j])
    if j > 0 and f[i][j-1] is c:
        count_link(i,j-1,f,link)
    if j < 5 and f[i][j+1] is c:
        count_link(i,j+1,f,link)
    if i > 0 and f[i-1][j] is c:
        count_link(i-1,j,f,link)
    if i < 12 and f[i+1][j] is c:
        count_link(i+1,j,f,link) 
    return link

def count_all_link(f):
    link = []
    for i in range(13):
        for j in range(6):
            #お邪魔ぷよではなく，連結未確認
            if f[i][j] is not 0 and not in3DArray([i,j],link):
                link.append(count_link(i,j,copy2DArray(f),[]))
    return link

x = count_all_link(field)
view_field(field)

print(x)
print(len(x))
