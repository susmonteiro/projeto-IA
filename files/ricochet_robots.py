# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 89:
# 92456 Duarte Bento
# 92560 Susana Monteiro

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys

#DEBUG
from time import sleep
from copy import deepcopy

# GLOBAL VARS
vari = 0
varj = 0
sortedRobots = []
wallsH = []
wallsV = []

mode_flag = 0
gravityTarget = []
gravityQ1 = []
gravityQ2 = []
gravityQ3 = []
gravityQ4 = []
gravityVector = []

#MODES
QUAD_1 = 1
QUAD_2V = 2
QUAD_2H = 3
QUAD_4 = 4

WEIGHT = 0
INF = 999
RIGHT = 'r'
LEFT = 'l'
UP = 'u'
DOWN = 'd'
movements = [RIGHT, LEFT, UP, DOWN]
Q1 = 1
Q2 = 2
Q3 = 3
Q4 = 4


class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id
    
    def __eq__(self, other):
        return isinstance(other, RRState) and self.board == other.board
    
    def __hash__(self):
        return hash(self.board)


class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    
    def __init__(self, size: int, robots: list, target: list):
        self.size = size
        self.robots = dict()

        for (c, i, j) in robots:
            self.robots[c] = (eval(i)-1, eval(j)-1) 
        
        self.targetColor = target[0]
        self.targetPos = (eval(target[1])-1, eval(target[2])-1)  

    def __eq__(self, other):
        return isinstance(other, Board) and self.robots == other.robots
    
    def __hash__(self):
        return hash(tuple(self.robots.items()))

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        return tuple(map(lambda x: x+1, self.robots[robot]))

    def set_robot_position(self, robot: str, pos: tuple):
        self.robots[robot] = pos

    def getQuadrant2H(self, pos):
        if pos[0] < self.targetPos[0]:
            return [Q1]
        if pos[0] > self.targetPos[0]:
            return [Q2]
        if pos[0] == self.targetPos[0]:
            return [Q1, Q2]
            
    def getQuadrant2V(self, pos):
        if pos[1] < self.targetPos[1]:
            return [Q1]
        if pos[1] > self.targetPos[1]:
            return [Q2]
        if pos[1] == self.targetPos[1]:
            return [Q1, Q2]
            
    def getQuadrant4(self, pos):
        answer = []
        # Q1 not in-line
        if pos[0] <= self.targetPos[0] and pos[1] >= self.targetPos[1]:
            answer.append(Q1)
        # Q2 not in-line
        if pos[0] <= self.targetPos[0] and pos[1] <= self.targetPos[1]:
            answer.append(Q2)
        # Q3 not in-line
        if pos[0] >= self.targetPos[0] and pos[1] <= self.targetPos[1]:
            answer.append(Q3)
        # Q4 not in-line
        if pos[0] >= self.targetPos[0] and pos[1] >= self.targetPos[1]:
            answer.append(Q4)
        
        return answer
    
    def isPosEmpty(self, pos_i, pos_j):
        for robot in self.robots:
            # print(robot)
            # print(self.robots[robot])
            if pos_i == self.robots[robot][0] and pos_j == self.robots[robot][1]:
                return False
        return True

    def canMove(self, action: tuple):
        robot = action[0]
        mov = action[1]
        pos_i = self.robots[robot][0]
        pos_j = self.robots[robot][1]
        # print("can move:", pos_i, pos_j)
        
        if mov == RIGHT:
            return not(wallsV[pos_i][pos_j + 1]) \
                and self.isPosEmpty(pos_i, pos_j + 1)
        if mov == LEFT:
            return not(wallsV[pos_i][pos_j]) \
                and self.isPosEmpty(pos_i, pos_j - 1)
        if mov == UP:
            return not(wallsH[pos_i][pos_j]) \
                and self.isPosEmpty(pos_i - 1, pos_j)
        if mov == DOWN:
            return not(wallsH[pos_i + 1][pos_j]) \
                and self.isPosEmpty(pos_i + 1, pos_j)

    def findNextStop(self, robot: str, mov: str):
        pos_i = self.robots[robot][0]
        pos_j = self.robots[robot][1]
        # print("find next wall:", pos_i, pos_j)

        if mov == RIGHT:
            for j in range(pos_j + 1, self.size + 1):
                if wallsV[pos_i][j] or not(self.isPosEmpty(pos_i, j)):
                    return (pos_i, j - 1)
        if mov == LEFT:
            for j in range(pos_j, -1, -1):
                if wallsV[pos_i][j] or not(self.isPosEmpty(pos_i, j - 1)):
                    return (pos_i, j)
        if mov == UP:
            for i in range(pos_i, -1, -1):
                if wallsH[i][pos_j] or not(self.isPosEmpty(i - 1, pos_j)):     # walls prevent index out of range (in theory)
                    return (i, pos_j)
        if mov == DOWN:
            for i in range(pos_i + 1, self.size + 1):
                # print("Walls check pos:", i, pos_j)
                if wallsH[i][pos_j] or not(self.isPosEmpty(i, pos_j)):
                    return (i-1, pos_j)
            
    
    def printBoard(self):
        print("robots " + str(self.robots), "target "+ str(self.targetColor) + " " + str(self.targetPos),\
            "Walls H:" + str(wallsH), "walls V" + str(wallsV), sep='\n')
    
    def checkGoal(self):
        # print("targetPos", self.targetPos)        
        # print("robot", self.robots[self.targetColor])        
        return self.targetPos == self.robots[self.targetColor]    

    def hValue(self):
        totalGravity = 0
        # if only one Quadrant, returns the sum of all robots gravity using gravityTarget
        if mode_flag == QUAD_1:
            for (i, j) in self.robots.values():
                totalGravity += gravityTarget[i][j]
            return totalGravity
   
        # get the gravity of the targetColored robot position
        totalGravity += (gravityTarget[self.targetPos[0]][self.targetPos[1]])

        if mode_flag == QUAD_2H:
            Qlist = self.getQuadrant2H(self.targetPos)
            
            for c, (i, j) in self.robots.items():
                if c != self.targetColor:
                    tmpGravity = INF
                    for q in Qlist:
                        tmpGravity = min(tmpGravity, gravityVector[q][i][j])
                    totalGravity += tmpGravity*WEIGHT
             
        elif mode_flag == QUAD_2V:
            Qlist = self.getQuadrant2V(self.targetPos)
            
            for c, (i, j) in self.robots.items():
                if c != self.targetColor:
                    tmpGravity = INF
                    for q in Qlist:
                        tmpGravity = min(tmpGravity, gravityVector[q][i][j])
                    totalGravity += tmpGravity*WEIGHT

        elif mode_flag == QUAD_4:
            Qlist = self.getQuadrant4(self.targetPos)
            
            for c, (i, j) in self.robots.items():
                if c != self.targetColor:
                    tmpGravity = INF
                    for q in Qlist:
                        tmpGravity = min(tmpGravity, gravityVector[q][i][j])
                    totalGravity += tmpGravity*WEIGHT
            
        return totalGravity

    # TODO: outros metodos da classe



class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = RRState(board)
        # TODO: self.initial = ...
        pass

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []    # list of tuples ('color', 'mov')

        for robot in sortedRobots:
            # print("robot:", state.board.robot_position(robot))
            for move in movements:
                action = (robot, move)
                if state.board.canMove(action):
                    actions.append(action)
        return actions

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # print("Current Position: ", state.board.robots[action[0]])
        # print("Performing Action: ", action)
        # print("actions:", self.actions(state))
        # print("Last action:", state.board.symmetricAction)
        
        newBoard = deepcopy(state.board)
        newState = RRState(newBoard)
        pos = newState.board.findNextStop(action[0], action[1])
        newState.board.set_robot_position(action[0], pos)
        return newState
        # pos = state.board.findNextWall(action[0], action[1])
        # state.board.set_robot_position(action[0], pos)
        # # state.board.printBoard()
        # return state

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        # print("Check for goal")
        return state.board.checkGoal()
        
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        #print(node.solution())
        #print(node.state.board.hValue())
        #print("++++")
        #sleep(0.75)
        return node.state.board.hValue()




# =======================


def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    # TODO
    global wallsV
    global wallsH
    global WEIGHT
    file = open(filename, 'r')
    size = eval(file.readline())      # Read Board size from file  
    robots = []
    for _ in range(4):
        robots += [file.readline().split(" ")]
    target = file.readline().split(" ")
    numWalls = eval(file.readline())
    
    wallsH = [[0 for _ in range(size)] for _ in range(size + 1)] 
    wallsV = [[0 for _ in range(size + 1)] for _ in range(size)] 

    for i in range(size):
        wallsV[i][0] = 1
        wallsV[i][size] = 1
        wallsH[0][i] = 1
        wallsH[size][i] = 1

    for _ in range(numWalls):
        i, j, p = file.readline().split(" ")
        i = eval(i) - 1
        j = eval(j) - 1
        if p[-1] == '\n': 
            p = p[:-1]        # Removes newline at the end
        if (p == LEFT):
            wallsV[i][j] = 1
        elif (p == RIGHT):
            wallsV[i][j+1] = 1
        elif (p == UP):
            wallsH[i][j] = 1
        elif (p == DOWN):
            wallsH[i+1][j] = 1    
    
    WEIGHT = size + 1
    sortRobots(robots, target)
    genGravity( size, target)
    return Board(size, robots, target)


def propagateGravity(gravity, size):
    global vari
    global varj
    varj = 1
    vari = 1
    _propagateGravity(gravity, 0, 0, size)

    varj = -1
    _propagateGravity(gravity, 0, size-1, size)

    vari = -1
    _propagateGravity(gravity, size-1, size-1, size)

    varj = 1
    _propagateGravity(gravity, size-1, 0, size)

def _propagateGravity(gravity, i, j, size):  
    if (i >= size or j >= size or i < 0 or j < 0):
        return INF + 1

    elif (gravity[i][j] < INF):
        return gravity[i][j]

    else:
        gravity[i][j] = min(_propagateGravity(gravity, i+vari, j, size), _propagateGravity(gravity, i, j+varj, size)) + 1
        return gravity[i][j]


def genGravity(size, target):
    pos = (eval(target[1]) -1, eval(target[2])-1)    

    if (pos[0] == 0 or pos[0] == size-1) and (pos[1] == 0 or pos[1] == size-1):
        # corner
        genGravity1(size, pos)
        return
    elif (pos[1] == 0 or pos[1] == size-1): # and (pos[0] != 0 or pos[0] != size-1)
        #horizontal line
        genGravity2Horizontal(size, pos)
        return
    elif (pos[0] == 0 or pos[0] == size-1): # and (pos[1] != 0 or pos[1] != size-1)
        #vertical line
        genGravity2Vertical(size, pos)
        return
    else:
        genGravity4(size, pos)

    for g in gravityVector:
        propagateGravity(g, size) 
        """ for line in g:
            print(line)
        print() """

def genGravity1(size, pos):
    global gravityTarget, gravityVector, mode_flag
    gravityTarget = [[INF for _ in range(size)] for _ in range(size)] 

    # main
    for i in range(size):
        gravityTarget[i][pos[1]] = 1

    for j in range(size):
        gravityTarget[pos[0]][j] = 1

    gravityTarget[pos[0]][pos[1]] = 0

    mode_flag = QUAD_1 
    gravityVector.append(gravityTarget)

def genGravity2Horizontal(size, pos):
    global gravityQ1, gravityQ2, gravityVector, mode_flag
    genGravity1(size, pos)

    gravityQ1 = [[INF for _ in range(size)] for _ in range(size)] 
    gravityQ2 = [[INF for _ in range(size)] for _ in range(size)]

    # Q1
    for j in range(size):
        gravityQ1[pos[0] + 1][j] = 1

    # Q2
    for j in range(size):
        gravityQ2[pos[0] - 1][j] = 1

    mode_flag = QUAD_2H
    gravityVector.append(gravityQ1)
    gravityVector.append(gravityQ2)

def genGravity2Vertical(size, pos):
    global gravityQ1, gravityQ2, gravityVector, mode_flag
    genGravity1(size, pos)

    gravityQ1 = [[INF for _ in range(size)] for _ in range(size)] 
    gravityQ2 = [[INF for _ in range(size)] for _ in range(size)]

    # Q1
    for i in range(size):
        gravityQ1[i][pos[1] + 1] = 1

    # Q2
    for i in range(size):
        gravityQ2[i][pos[1] - 1] = 1

    mode_flag = QUAD_2V
    gravityVector.append(gravityQ1)
    gravityVector.append(gravityQ2)

def genGravity4(size, pos):
    global gravityQ1, gravityQ2, gravityQ3, gravityQ4, gravityVector, mode_flag
    
    gravityQ1 = [[INF for _ in range(size)] for _ in range(size)] 
    gravityQ2 = [[INF for _ in range(size)] for _ in range(size)] 
    gravityQ3 = [[INF for _ in range(size)] for _ in range(size)] 
    gravityQ4 = [[INF for _ in range(size)] for _ in range(size)] 

    genGravity1(size, pos)

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

    mode_flag = QUAD_4
    gravityVector.append(gravityQ1)
    gravityVector.append(gravityQ2)
    gravityVector.append(gravityQ3)
    gravityVector.append(gravityQ4)
    





def sortRobots(robots, target):
    # first: target colored robot
    global sortedRobots
    sortedRobots.append(target[0])
    for (robotC, _, _) in robots:
        if robotC != target[0]:
            sortedRobots.append(robotC)

def printSolve(res):
    resMoves = res.solution()
    print(len(resMoves))
    for tpl in resMoves:
        print(tpl[0], tpl[1])

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    board = parse_instance(sys.argv[1])
    res = astar_search(RicochetRobots(board))
    printSolve(res)

    ###
    # if len(node.solution()) > 2 and (node.solution()[0] == ('B', 'l')) and (node.solution()[1] == ('Y', 'u')) and (node.solution()[2] == ('R', 'r')):
    #     print()
    #     print(node.solution())
    #     print()
    #     print(problem.goal_test(node.state))
    #     print(node.state.board.robot_position('R'))
    #     sleep(0.1)
    ###