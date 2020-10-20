#!/bin/bash

INPUTDIR=instances

for fin in $INPUTDIR/*; do 
	echo "======${fin}========"
	timeout 30 python ricochet_robots_allS.py $fin a
	timeout 30 python ricochet_robots_allS.py $fin g
	timeout 30 python ricochet_robots_allS.py $fin b
	timeout 30 python ricochet_robots_allS.py $fin d
done
