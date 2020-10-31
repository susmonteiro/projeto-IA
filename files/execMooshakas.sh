#!/bin/bash

INPUTDIR=testes/testes_verificacao_solucao
failcount=0
filecount=0
for fin in $INPUTDIR/*; do 
    # echo "======${fin}========"
    let filecount=filecount+1 
    #/usr/bin/time -f "%M\n%E" timeout 30 python manhattan.py $fin || let failcount=failcount+1
    # /usr/bin/time -f "%M\n%E" timeout 30 python3 ricochet_robots.py $fin || let failcount=failcount+1
    /usr/bin/time -f "%M\t%E" python3 distanceManhattan.py $fin || echo -e "\033[91mFAILED======${fin}========\033[0m"
    # timeout 30 python3 ricochet_robots_allS.py $fin d
    # timeout 30 python3 ricochet_robots_allS.py $fin g
    # timeout 30 python3 ricochet_robots_allS.py $fin a
done
echo "passed $(expr ${filecount} - ${failcount}) in ${filecount}"

