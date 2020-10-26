import os
from random import randint
from parse import compile
import threading

# [(Rmin, Rmax), SCmin]
ranges = [[(1000, 5000), 900],[(pow(10,4), 5*pow(10,4)), 9*pow(10,3)],[(pow(10,5), 2*pow(10,5)), 9*pow(10,4)]]
nPoints = 10
data = []
threads = []
ping = [False]
mutex = threading.Lock()

class myThread (threading.Thread):
   def __init__(self, times, i, flag):
        threading.Thread.__init__(self)
        self.times = times
        self.i = i
        self.flag = flag
   def run(self):
       create(self.times, self.i, self.flag)


def create(times, i, ping):
    # generator
        print("TEST " + str(i))
        M = 100
        N = i // M
        M = str(M)
        N = str(N)
        args = "-n " + N + " -m " + M + " -N " + N + " -M " + M

        mutex.acquire()
        flagIN = ping[0]
        ping[0] = not(ping[0])
        mutex.release()

        if flagIN:
            S = str(ranges[times][1])
            C = str(randint(ranges[times][1], i))
        else:
            C = str(ranges[times][1])
            S = str(randint(ranges[times][1], i))
        
        
        args += " -s " + S + " -c " + C + " -S " + S + " -C " + C
        generatorCmd = "python2.7 p2_gerador.py " + args + " > exp/" + str(i) + ".in"
        os.system(generatorCmd)
        
        # dfs
        dfsCmd = "(time ./dfs.out < exp/"+ str(i) + ".in" + "> exp/dfs"+ str(i) + ".out) 2> exp/dfs" + str(i) + ".res"
        os.system(dfsCmd)
        
        # bfs
        bfsCmd = "(time ./bfs.out < exp/"+ str(i) + ".in" + "> exp/bfs"+ str(i) + ".out) 2> exp/bfs" + str(i) + ".res"
        os.system(bfsCmd)





for times in range(len(ranges)):
    print("\n============ TRIAL " + str(times) + " ============")
    #create
    for i in range(ranges[times][0][0], ranges[times][0][1], (ranges[times][0][1]-ranges[times][0][0])//nPoints):
        threadi = myThread(times, i, ping)
        threadi.start()
        threads.append(threadi)

    for t in threads:
        t.join()
    
    #process
    for i in range(ranges[times][0][0], ranges[times][0][1], (ranges[times][0][1]-ranges[times][0][0])//nPoints):
        iData = []
        # generator size
        generatorFp = open("exp/" + str(i) + ".in", "r")
        splited = generatorFp.readline().split()
        splited += generatorFp.readline().split()
        iData += [val for val in splited]
        generatorFp.close()

        # dfs
        dfsFp = open("exp/dfs"+ str(i) + ".out", "r")
        dfsRes = eval(dfsFp.readline().split()[0])
        dfsTimes = dfsFp.readline().split()[2]
        iData += ["DfsVisits " + dfsTimes]
        dfsFp.close()

        # bfs
        bfsFp = open("exp/bfs"+ str(i) + ".out", "r")
        bfsRes = eval(bfsFp.readline().split()[0])
        bfsTimes = bfsFp.readline().split()[2]
        iData += ["BfsVisits "+ bfsTimes]
        bfsFp.close()

        # time
        timeDfsFp = open("exp/dfs"+ str(i) + ".res", "r")
        timeBfsFp = open("exp/bfs"+ str(i) + ".res", "r")
        p_content = compile("real\t{}s")
        for line in timeDfsFp.readlines():
            if "real" in line:
                dfsTime = p_content.parse(line)[0]
                iData += ["dfsTime "+ dfsTime]
        for line in timeBfsFp.readlines():
            if "real" in line:
                bfsTime = p_content.parse(line)[0]
                iData += ["bfsTime "+ bfsTime] 

        timeDfsFp.close()        
        timeBfsFp.close()

        # checks
        if dfsRes != bfsRes:
            print("WARNING " + str(i))
        if eval(dfsTimes) > eval(bfsTimes):
            print("STUPID DFSSSSSS " + str(i))
        
        # Update data
        data += [iData]

        for lst in iData:
            print(lst, end=" | ")
        print()

