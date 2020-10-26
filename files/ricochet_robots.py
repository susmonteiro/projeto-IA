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

INF = 999
RIGHT = 'r'
LEFT = 'l'
UP = 'u'
DOWN = 'd'
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


class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    
    def __init__(self, size: int, robots: list, target: list):
        self.size = size
        self.robots = dict()

        for (c, i, j) in robots:
            self.robots[c] = (eval(i)-1, eval(j)-1) 
        
        self.targetColor = target[0]
        self.targetPos = (eval(target[1])-1, eval(target[2])-1)  

        ###
        self.symmetricAction = tuple()

    def set_lastAction(self, tpl: tuple):
        self.symmetricAction = (tpl[0], self.symmetricMove(tpl[1]))

    def symmetricMove(self, move: str):
        if move == RIGHT:
            return LEFT
        if move == LEFT:
            return RIGHT
        if move == UP:
            return DOWN
        if move == DOWN:
            return UP
        
    def check_notSymmetricAction(self, action: tuple):
        return not(action == self.symmetricAction)

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        return tuple(map(lambda x: x+1, self.robots[robot]))

    def set_robot_position(self, robot: str, pos: tuple):
        # print("inside set robot pos", robot)
        # print(pos)
        self.robots[robot] = pos
    
    
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

        #TODO check if symmetric to the lastAction
        
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

    def distanceFromTarget(self, robotC):
        return abs(self.targetPos[0] - self.robots[robotC][0]) + \
            abs(self.targetPos[1] - self.robots[robotC][1])

    def hValue(self):
        total = 0
        for robotC in self.robots.keys():
            total += self.distanceFromTarget(robotC)
        return total
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
        movements = [RIGHT, LEFT, UP, DOWN]

        for robot in sortedRobots:
            # print("robot:", state.board.robot_position(robot))
            for move in movements:
                action = (robot, move)
                if state.board.check_notSymmetricAction(action) and state.board.canMove(action):
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
        newState.board.set_lastAction(action)
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
        return node.state.board.hValue()




# =======================


def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    # TODO
    global wallsV
    global wallsH
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
    
    sortRobots(robots, target)
    return Board(size, robots, target)


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