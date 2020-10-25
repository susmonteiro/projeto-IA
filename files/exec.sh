#!/bin/bash

INPUTDIR=testes/more-rr-tests
failcount=0
filecount=0
for dir in $INPUTDIR/*; do 
	for fin in $dir/*; do 
		echo "======${dir}/${fin}========"
		let filecount=filecount+1 
		timeout 30 python ricochet_robots_allS.py $fin a || let failcount=failcount+1
		# timeout 30 python ricochet_robots_allS.py $fin g
		# timeout 30 python ricochet_robots_allS.py $fin b
		# timeout 30 python ricochet_robots_allS.py $fin d
	done
done

echo "passed $(expr ${filecount} - ${failcount}) in ${filecount}"
