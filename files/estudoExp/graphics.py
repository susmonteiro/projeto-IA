import os
from random import randint
from parse import compile
import matplotlib.pyplot as plt
import numpy as np

# [(Rmin, Rmax), SCmin]
ranges = [[(1000, 5000), 900],[(pow(10,4), 5*pow(10,4)), 9*pow(10,3)],[(pow(10,5), 2*pow(10,5)), 9*pow(10,4)]]
nPoints = 10
data = []

for times in range(len(ranges)):
    #process
    dfsx = []
    dfsy = []
    dfsvt = []
    bfsx = []
    bfsy = []
    bfsvt = []
    for i in range(ranges[times][0][0], ranges[times][0][1], (ranges[times][0][1]-ranges[times][0][0])//nPoints):
        iData = []
        dfsx.append(i)
        bfsx.append(i)

        # generator size
        generatorFp = open("exp/" + str(i) + ".in", "r")
        splited = generatorFp.readline().split()
        splited += generatorFp.readline().split()
        iData += [val for val in splited]
        generatorFp.close()

        # dfs
        dfsFp = open("exp/dfs"+ str(i) + ".out", "r")
        dfsres = eval(dfsFp.readline().split()[0])
        dfsTimes = dfsFp.readline().split()[2]
        iData += ["DfsVisits " + dfsTimes]
        dfsFp.close()
        dfsvt.append(eval(dfsTimes))

        # bfs
        bfsFp = open("exp/bfs"+ str(i) + ".out", "r")
        bfsres = eval(bfsFp.readline().split()[0])
        bfsTimes = bfsFp.readline().split()[2]
        iData += ["BfsVisits "+ bfsTimes]
        bfsFp.close()
        bfsvt.append(eval(bfsTimes))
        
        # time
        timeDfsFp = open("exp/dfs"+ str(i) + ".res", "r")
        timeBfsFp = open("exp/bfs"+ str(i) + ".res", "r")
        p_content = compile("real\t{}m{}s")
        for line in timeDfsFp.readlines():
            if "real" in line:
                vals = p_content.parse(line)
                mins = vals[0]
                secs = vals[1].replace(",", ".")
                print(secs)
                totalSecs = eval(mins)*60 + eval(secs)
                print(totalSecs)
                dfsy.append(totalSecs)
                iData += ["dfsTime "+ str(totalSecs)]
        for line in timeBfsFp.readlines():
            if "real" in line:
                vals = p_content.parse(line)
                mins = vals[0]
                secs = vals[1].replace(",", ".")
                totalSecs = eval(mins)*60 + eval(secs)
                print(totalSecs)
                bfsy.append(totalSecs)
                iData += ["bfsTime "+ str(totalSecs)]

        timeDfsFp.close()        
        timeBfsFp.close()

        # checks
        if dfsres != bfsres:
            print("WARNING " + str(i))
        if eval(dfsTimes) > eval(bfsTimes):
            print("STUPID DFSSSSSS " + str(i))
        
        # Update data
        data += [iData]

    # Generating Graphic
    print(dfsx, dfsy, sep="\n\n")
    fig = plt.figure()
    ax = fig.add_subplot(111)

    z = np.polyfit(dfsx, dfsy, 1)
    p = np.poly1d(z)
    plt.plot(dfsx,p(dfsx),"b--", label="trend Dfs")
    ax.plot(dfsx, dfsy, label="Dfs")  # Plot some data on the axes.
    
    z = np.polyfit(bfsx, bfsy, 1)
    p = np.poly1d(z)
    plt.plot(bfsx,p(bfsx), color="orange", ls="--", label="trend Bfs")
    ax.plot(bfsx, bfsy, label="Bfs")

    plt.xlabel("Número de Vértices (M*N)")
    plt.ylabel("Tempo de Execução (s)")
    plt.title("Tempo em ordem ao Tamanho da Matriz (min{S,C}="+str(ranges[times][1]) + ")", fontsize=12)
    plt.legend()
    fig.savefig("plotWBfs"+str(times)+".png")


