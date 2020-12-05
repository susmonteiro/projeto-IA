from ricochet_robots import *

from os import listdir

sortedLst = listdir("instances")
sortedLst.sort()

sortedLst = map(lambda s: "instances/"+s, sortedLst)

for f in sortedLst:
        print("==========", f, "==========")
        print("==========", "A*", "==========")
        board = parse_instance(f)
        sortRobots(sortedRobots, board)
        res = astar_search(RicochetRobots(board))
        resMoves = res.solution()
        print(len(resMoves))
        for tpl in resMoves:
                print(tpl[0], tpl[1])
for f in sortedLst:
        print("==========", f, "==========")
        print("==========", "Greedy", "==========")
        board = parse_instance(f)
        sortRobots(sortedRobots, board)
        res = greedy_search(RicochetRobots(board))
        resMoves = res.solution()
        print(len(resMoves))
        for tpl in resMoves:
                print(tpl[0], tpl[1])
for f in sortedLst:
        print("==========", f, "==========")
        print("==========", "BFS", "==========")
        board = parse_instance(f)
        sortRobots(sortedRobots, board)
        res = breadth_first_tree_search(RicochetRobots(board))
        resMoves = res.solution()
        print(len(resMoves))
        for tpl in resMoves:
                print(tpl[0], tpl[1])
for f in sortedLst:
        print("==========", f, "==========")
        print("==========", "DFS", "==========")
        board = parse_instance(f)
        sortRobots(sortedRobots, board)
        res = depth_first_tree_search(RicochetRobots(board))
        resMoves = res.solution()
        print(len(resMoves))
        for tpl in resMoves:
                print(tpl[0], tpl[1])

        # res = depth_first_tree_search(RicochetRobots(board))