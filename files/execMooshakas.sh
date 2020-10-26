#!/bin/bash

INPUTDIR=testes/testes_verificacao_solucao
failcount=0
filecount=0
for fin in $INPUTDIR/*; do 
    echo "======${fin}========"
    let filecount=filecount+1 
    /usr/bin/time -f "%M\n%E" timeout 30 python manhattan.py $fin || let failcount=failcount+1
    /usr/bin/time -f "%M\n%E" timeout 30 python ricochet_robots2.py $fin || let failcount=failcount+1
    # timeout 30 python ricochet_robots_allS.py $fin g
    # timeout 30 python ricochet_robots_allS.py $fin b
    # timeout 30 python ricochet_robots_allS.py $fin d
    echo "passed $(expr ${filecount} - ${failcount}) in ${filecount}"
done

