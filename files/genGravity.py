from time import sleep

def genGravity(gravity, i, j):  
    if (i == size or j == size or i == -1 or j == -1):
        return INF + 1

    elif (gravity[i][j] < INF):
        return gravity[i][j]

    else:
        gravity[i][j] = min(genGravity(gravity, i+vari, j), genGravity(gravity, i, j+varj)) + 1
        return gravity[i][j]


def _genGravity(gravity):
    global vari
    global varj
    varj = 1
    vari = 1
    genGravity(gravity, 0,0)

    varj = -1
    genGravity(gravity, 0, size-1)

    vari = -1
    genGravity(gravity, size-1, size-1)

    varj = 1
    genGravity(gravity, size-1, 0)


vari = 0
varj = 0
INF = 999
size = 6
pos = (4,3)
gravityTarget = [[INF for _ in range(size)] for _ in range(size)] 
gravityQ1 = [[INF for _ in range(size)] for _ in range(size)] 
gravityQ2 = [[INF for _ in range(size)] for _ in range(size)] 
gravityQ3 = [[INF for _ in range(size)] for _ in range(size)] 
gravityQ4 = [[INF for _ in range(size)] for _ in range(size)] 
gravityV = [gravityTarget, gravityQ1, gravityQ2, gravityQ3, gravityQ4]


for i in range(size):
    gravityTarget[i][pos[1]] = 1

for j in range(size):
    gravityTarget[pos[0]][j] = 1

gravityTarget[pos[0]][pos[1]] = 0


# Q1
for i in range(pos[0]+1):
    gravityQ1[i][pos[1] - 1] = 1

for j in range(pos[1], size):
    gravityQ1[pos[0] + 1][j] = 1

# Q2
for i in range(pos[0]+1):
    gravityQ2[i][pos[1] + 1] = 1

for j in range(pos[1] + 1):
    gravityQ2[pos[0] + 1][j] = 1

# Q3
for i in range(pos[0], size):
    gravityQ3[i][pos[1] + 1] = 1

for j in range(pos[1] + 1):
    gravityQ3[pos[0] - 1][j] = 1

# Q4
for i in range(pos[0], size):
    gravityQ4[i][pos[1] - 1] = 1

for j in range(pos[1], size):
    gravityQ4[pos[0] - 1][j] = 1




i = 1
for q in gravityV:
    _genGravity(q)
    print("Gravity", i)
    for line in q:
        print(line)
    i += 1

'''

 _ _ _
| | | |
| | | |
| | | |
 _ _ _


'''


