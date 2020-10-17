# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 89:
# 92456 Duarte Bento
# 92560 Susana Monteiro

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys

# GLOBAL VARS
sortedRobots = []


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
    RIGHT = 'r'
    LEFT = 'l'
    UP = 'u'
    DOWN = 'd' 
    
    def __init__(self, size: int, robots: list, target: list,  wallsH: list, wallsV:list):
        self.size = size
        self.robots = dict()

        for (c, i, j) in robots:
            self.robots[c] = (eval(i)-1, eval(j)-1) 
        
        self.targetColor = target[0]
        self.targetPos = (eval(target[1])-1, eval(target[2])-1)  
        self.wallsH = wallsH
        self.wallsV = wallsV
        
    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        return self.robots[robot]

    def set_robot_position(self, robot: str, pos: tuple):
        self.robots[robot] = (pos[0], pos[1])

    def canMove(self, robot: str, mov: str):
        pos_i = self.robots[robot][0]
        pos_j = self.robots[robot][1]
        
        if mov == self.RIGHT:
            return not(self.wallsV[pos_i][pos_j + 1])
        if mov == self.LEFT:
            return not(self.wallsV[pos_i][pos_j])
        if mov == self.UP:
            return not(self.wallsH[pos_i][pos_j])
        if mov == self.DOWN:
            return not(self.wallsH[pos_i + 1][pos_j])

    def findNextWall(self, robot: str, mov: str):
        pos_i = self.robots[robot][0]
        pos_j = self.robots[robot][1]

        if mov == self.RIGHT:
            for j in range(pos_j + 1, self.size + 1):
                if self.wallsV[pos_i][j]:
                    return (pos_i, j)
        if mov == self.LEFT:
            for j in range(pos_j, -1, -1):
                if self.wallsV[pos_i][j]:
                    return (pos_i, j)
        if mov == self.UP:
            for i in range(pos_i, -1, -1):
                if self.wallsH[i][pos_j]:
                    return (i, pos_j)
        if mov == self.DOWN:
            for i in range(pos_i + 1, self.size + 1):
                if self.wallsH[i][pos_j]:
                    return (i, pos_j)
            
    
    def printBoard(self):
        print("robots " + str(self.robots), "target "+ str(self.targetColor) + " " + str(self.targetPos),\
            "Walls H:" + str(self.wallsH), "walls V" + str(self.wallsV), sep='\n')
    
    def checkGoal(self):
        return self.targetPos == self.robots[self.targetColor]    

    
    # TODO: outros metodos da classe


def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    # TODO
    file = open(filename, 'r')
    size = eval(file.readline())      # Read Board size from file  
    robots = []
    for _ in range(4):
        robots += [file.readline().split(" ")]
    target = file.readline().split(" ")
    numWalls = eval(file.readline())
    
    horizontal = [[0 for _ in range(size)] for _ in range(size + 1)] 
    vertical = [[0 for _ in range(size + 1)] for _ in range(size)] 

    for i in range(size):
        vertical[i][0] = 1
        vertical[i][size] = 1
        horizontal[0][i] = 1
        horizontal[size][i] = 1

    for _ in range(numWalls):
        i, j, p = file.readline().split(" ")
        i = eval(i) - 1
        j = eval(j) - 1
        p = p[:-1]        # Removes newline at the end
        if (p == Board.LEFT):
            vertical[i][j] = 1
        elif (p == Board.RIGHT):
            vertical[i][j+1] = 1
        elif (p == Board.UP):
            horizontal[i][j] = 1
        elif (p == Board.DOWN):
            horizontal[i+1][j] = 1
    return Board(size, robots, target, horizontal, vertical)




class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = board
        # TODO: self.initial = ...
        pass

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []    # list of tuples ('color', 'mov')
        
        for robot in sortedRobots:
            if state.board.canMove(robot, Board.RIGHT):
                actions += (robot, Board.RIGHT)
            if state.board.canMove(robot, Board.LEFT):
                actions += (robot, Board.LEFT)
            if state.board.canMove(robot, Board.UP):
                actions += (robot, Board.UP)
            if state.board.canMove(robot, Board.DOWN):
                actions += (robot, Board.DOWN)
        
        return actions

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        newBoard = copy.deepcopy(state.board)
        pos = state.board.findNextWall(action[0], action[1])
        newBoard.set_robot_position(pos[0], pos[1])
        newState = RRState(newBoard)
        return newState

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        return state.board.checkGoal()
        
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass

def sortRobots(lst: list, board: Board):
        # first: target colored robot
        lst.append(board.targetColor)
        for robotC in board.robots.keys():
            if robotC != board.targetColor:
                sortedRobots.append(robotC)



if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    board = parse_instance("i1.txt")
    sortRobots(sortedRobots, board)
    board.printBoard()

    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
