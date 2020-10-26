#!/bin/bash                      
g++ -std=c++11 -O3 -Wall main.cpp -lm -o 1dfs.out> /dev/null 2>&1
g++ -std=c++11 -O3 -Wall bimain.cpp -lm -o 1bfs.out> /dev/null 2>&1
#-n -N min, max number of streets
#-m -M min, max number of avenues
#-S max number of shops
#-C max number of clients
python2.7 p2_gerador.py -n $1 -m $2 -N $1 -M $2 -S $3 -C $4 > input
echo "input file:"
cat input
python3 matrixVisualizer.py input
echo "project DFS output:"
./1dfs.out < input
echo "project BFS output:"
./1bfs.out < input
