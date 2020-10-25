#!/bin/bash

INPUTDIR=testes/testes_verificacao_solucao
failcount=0
filecount=0
for fin in $INPUTDIR/*; do 
	echo "======${fin}========"
	let filecount=filecount+1 
	timeout 30 python ricochet_robots_allS.py $fin a || let failcount=failcount+1
	# timeout 30 python ricochet_robots_allS.py $fin g
	# timeout 30 python ricochet_robots_allS.py $fin b
	# timeout 30 python ricochet_robots_allS.py $fin d
done

echo "passed $(expr ${filecount} - ${failcount}) in ${filecount}"
