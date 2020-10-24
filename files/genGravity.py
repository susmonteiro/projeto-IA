from time import sleep

def genGravity(i, j):  
        #sleep(0.5)     
        #print(i, j)

        if (i == size or j == size):
            #print("INFINITO")
            return INF + 1

        elif (pos == (i, j)):
            #print("TARGET")
            gravity[i][j] = 0
            return 0

        elif (i == pos[0] or j == pos[1]):
            #print("LINHA")
            gravity[i][j] = 1
            return 1

        elif (gravity[i][j] < INF):
            #print("ME")
            return gravity[i][j]

        else:
            #print("ELSE")
            #gravity[i][j] = min(genGravity(i+1, j), genGravity(i, j+1)) + 1
            gravity[i][j] = min(genGravity(i+vari, j), genGravity(i, j+varj)) + 1
                #genGravity(i, j-1), genGravity(i-1, j)) + 1
            #print(gravity)
            return gravity[i][j]

        #elif (gravity[i][j] < INF):
        #    print(gravity[i][j])
        #    return gravity[i][j] """

INF = 999
size = 6
pos = (3,2)
gravity = [[INF for _ in range(size)] for _ in range(size)] 

vari = 1
varj = 1
genGravity(0,0)

varj = -1
genGravity(0, size-1)

vari = -1
genGravity(size-1, size-1)

varj = 1
genGravity(size-1, 0)

gravity[pos[0]][pos[1]] = 0

#[[ genGravity(i, j) for i in range(size)] for j in range(size)]
print(gravity)

'''
 _ _ _
| | | |
| | | |
| | | |
 _ _ _


'''


