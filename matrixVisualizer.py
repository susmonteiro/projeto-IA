'''
INPUT:
NAv MStr
NShop NClient
NShop*lines
NClient*lines
'''
import sys

BLACK = 0
SHOP = 1
CLIENT = 2

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

filename = sys.argv[1]

fp = open(filename, "r")

NAv, NStr = map(eval, fp.readline().split(" "))
NShop, NClient = map(eval, fp.readline().split(" "))


Matrix = [["e" for j in range(NStr)] for i in range(NAv)]

for _ in range(NShop):
    x,y = map(eval, fp.readline().split(" "))
    x -=1
    y -=1
    Matrix[x][y] = 's'

for _ in range(NClient):
    x,y = map(eval, fp.readline().split(" "))
    x -=1
    y -=1
    if (Matrix[x][y] != 's' and Matrix[x][y] != 'b'):
        Matrix[x][y] = 'c'
    else:
        Matrix[x][y] = 'b'


def printEl(El):
    if El == 'e':
        print("●", end='')
    elif El == 's':
        print(bcolors.OKGREEN + "●" + bcolors.ENDC, end='')
    elif El == 'c':
        print(bcolors.WARNING + "●" + bcolors.ENDC, end='')
    else:
        print(bcolors.FAIL + "●" + bcolors.ENDC, end='')

print('\t', end='')
for column in range(NStr):
        print(str(column+1) , end='   ')
print()

for line in range(NAv):
    print(line+1, end='\t')
    for column in range(NStr):
        if(column == NStr-1):
            printEl(Matrix[line][column])
        else:
            printEl(Matrix[line][column])
            print(' - ', end='')

    print('\n\t', end='')
    if line != NAv - 1:
        for column in range(NStr):
            print("|   ", end='')
        print()

print()