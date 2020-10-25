# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 89:
# 92456 Duarte Bento
# 92560 Susana Monteiro

from ricochet_robots import *

def printSolve(res):
    resMoves = res.solution()
    print(len(resMoves))
    for tpl in resMoves:
        print(tpl[0], tpl[1])

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    board = parse_instance(sys.argv[1])
    if sys.argv[2] == "a":
        print("==========", "Astar", "==========")
        res = astar_search(RicochetRobots(board))
        printSolve(res)   
    if sys.argv[2] == "g":
        print("==========", "Greedy", "==========")
        res = greedy_search(RicochetRobots(board))
        printSolve(res)  
    if sys.argv[2] == "d":
        print("==========", "dfs", "==========")
        res = depth_first_tree_search(RicochetRobots(board))
        printSolve(res)
    if sys.argv[2] == "b":
        print("==========", "bfs", "==========")
        res = breadth_first_tree_search(RicochetRobots(board))
        printSolve(res)

    # ###
    # if len(node.solution()) > 2 and (node.solution()[0] == ('B', 'l')) and (node.solution()[1] == ('Y', 'u')) and (node.solution()[2] == ('R', 'r')):
    #     print()
    #     print(node.solution())
    #     print()
    #     print(problem.goal_test(node.state))
    #     print(node.state.board.robot_position('R'))
    #     sleep(0.1)
    # ###
