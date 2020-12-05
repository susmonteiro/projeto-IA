# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 89:
# 92456 Duarte Bento
# 92560 Susana Monteiro

from ricochet_robots import *
import time
import resource 

def printSolve(res):
    resMoves = res.solution()
    print(len(resMoves))
    for tpl in resMoves:
        print(tpl[0], tpl[1])

  
def limit_memory(maxsize): 
    soft, hard = resource.getrlimit(resource.RLIMIT_AS) 
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard)) 


def Astar(board):
    p = InstrumentedProblem(RicochetRobots(deepcopy(board)))
    start = time.time()
    res = astar_search(p)
    delta = time.time() - start
    #printSolve(res, delta)   
    print(p.succs, p.states, delta, sep="\t", end='\t')

def Greedy(board):
    p = InstrumentedProblem(RicochetRobots(deepcopy(board)))
    start = time.time()
    res = greedy_search(p)
    delta = time.time() - start
    #printSolve(res, delta)  
    print(p.succs, p.states, delta, sep="\t", end='\t')

def Dfs(board):
    p = InstrumentedProblem(RicochetRobots(deepcopy(board)))
    start = time.time()
    res = depth_first_tree_search(RicochetRobots(board))
    delta = time.time() - start
    #printSolve(res, delta)
    print(p.succs, p.states, delta, sep="\t", end='\t') 

def Bfs(board):
    p = InstrumentedProblem(RicochetRobots(deepcopy(board)))
    start = time.time()
    res = breadth_first_tree_search(p)
    delta = time.time() - start
    #printSolve(res)
    print(p.succs, p.states, delta, sep="\t", end='\t')



if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    limit_memory(4 * 2**20)
    board = parse_instance(sys.argv[1])
    if len(sys.argv) == 2:
        Astar(board)
        Greedy(board)
        Dfs(board)
        Bfs(board)
    else:
        if sys.argv[2] == "a":
            Astar(board)
        if sys.argv[2] == "g":
            Greedy(board)
        if sys.argv[2] == "d":
            Dfs(board)
        if sys.argv[2] == "b":
            Bfs(board)

    # ###
    # if len(node.solution()) > 2 and (node.solution()[0] == ('B', 'l')) and (node.solution()[1] == ('Y', 'u')) and (node.solution()[2] == ('R', 'r')):
    #     print()
    #     print(node.solution())
    #     print()
    #     print(problem.goal_test(node.state))
    #     print(node.state.board.robot_position('R'))
    #     sleep(0.1)
    # ###
