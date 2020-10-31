# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 89:
# 92456 Duarte Bento
# 92560 Susana Monteiro

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search, InstrumentedProblem
import sys

#DEBUG
from copy import deepcopy
from math import sqrt

# GLOBAL VARS
INF = 0
WEIGHT = 0
sortedRobots = []
wallsH = []
wallsV = []
gravity = []

RIGHT = 'r'
LEFT = 'l'
UP = 'u'
DOWN = 'd'

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

    
    def isPosEmpty(self, pos_i, pos_j):
        for robot in self.robots:
            if pos_i == self.robots[robot][0] and pos_j == self.robots[robot][1]:
                return False
        return True

    def canMove(self, action: tuple):
        robot = action[0]
        mov = action[1]
        pos_i = self.robots[robot][0]
        pos_j = self.robots[robot][1]
        
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
                if wallsH[i][pos_j] or not(self.isPosEmpty(i, pos_j)):
                    return (i-1, pos_j)
            
    
    def printBoard(self):
        print("robots " + str(self.robots), "target "+ str(self.targetColor) + " " + str(self.targetPos),\
            "Walls H:" + str(wallsH), "walls V" + str(wallsV), sep='\n')
    
    def checkGoal(self):      
        return self.targetPos == self.robots[self.targetColor]    

    def hValue(self):
        # get the gravity of the targetColored robot position
        totalGravity = 0
        for (i, j) in self.robots.values():
            totalGravity += gravity[i][j]            
        return WEIGHT*totalGravity




class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = RRState(board)
        pass

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []    # list of tuples ('color', 'mov')
        movements = [RIGHT, LEFT, UP, DOWN]

        for robot in sortedRobots:
            
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
        newBoard = deepcopy(state.board)
        newState = RRState(newBoard)
        pos = newState.board.findNextStop(action[0], action[1])
        newState.board.set_robot_position(action[0], pos)
        return newState

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        return state.board.checkGoal()
        
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        return node.state.board.hValue()




# =======================


def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    global wallsV
    global wallsH
    global WEIGHT
    global INF
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

    INF = size
    WEIGHT = sqrt(size)

    sortRobots(robots, target)
    genGravity(size, target)
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
        if wallsH[i+max(vari, 0)][j]:
            if wallsV[i][j+max(varj, 0)]:
                return gravity[i][j]
            else:
                gravity[i][j] = _propagateGravity(gravity, i, j+varj, size) + 1
        elif wallsV[i][j+max(varj, 0)]:
            gravity[i][j] = _propagateGravity(gravity, i+vari, j, size) + 1
        else:
            gravity[i][j] = min(_propagateGravity(gravity, i+vari, j, size), _propagateGravity(gravity, i, j+varj, size)) + 1
        return gravity[i][j]


def genGravity(size, target):
    pos = (eval(target[1]) -1, eval(target[2])-1)    
    global gravity
    gravity = [[INF for _ in range(size)] for _ in range(size)] 

    for i in range(pos[0]-1, -1, -1):
        if wallsH[i+1][pos[1]]:
            break
        gravity[i][pos[1]] = 1
    
    for i in range(pos[0]+1, size):
        if wallsH[i][pos[1]]:
            break
        gravity[i][pos[1]] = 1

    for j in range(pos[1]-1, -1, -1):
        if wallsV[pos[0]][j+1]:
            break
        gravity[pos[0]][j] = 1

    for j in range(pos[1]+1, size):
        if wallsV[pos[0]][j]:
            break
        gravity[pos[0]][j] = 1

    gravity[pos[0]][pos[1]] = 0

    propagateGravity(gravity, size) 



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
    # Ler o ficheiro de input de sys.argv[1],
    board = parse_instance(sys.argv[1])
    p = InstrumentedProblem(RicochetRobots(board))
    res = astar_search(p)
    # printSolve(res)
    # print("Expanded:", p.succs, "|| Generated:", p.states, "|| Sum:", p.succs + p.states)
