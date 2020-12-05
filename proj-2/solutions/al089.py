# -*- coding: utf-8 -*-
"""
Grupo al089
Student id #92456
Student id #92560
"""
import numpy as np
from math import log

## GLOBAL

attrValues = []


def importance(p, n):
	posFraction = p/(n+p)
	negFraction = n/(n+p)
	if p == 0 or n == 0:
		return 0
	elif p == 1/2:
		return 1
	else:
		return abs(posFraction*log(posFraction, 2) + negFraction*log(negFraction, 2))

def calculateRest(D, Y, a_idx, totalP, totalN):
	''' Calculate the sum of the rest for a  given attribute '''
	attrVect = attrValues[a_idx]
	rest = 0

	# calculate importance for each value of attr
	for v in attrVect:
		filteredY = []

		# get classification of lines where attr = v
		for idx in len(D):
			if D[idx][a_idx] == v:
				filteredY.append(Y[idx])	
		
		p, n = countP_N(filteredY)
		rest += ((p + n)/(totalP, totalN))*importance(p, n)

	return rest


def maxGain(D, Y, attr):
	totalP, totalN = countP_N(Y) 
	totalImportance = importance(totalP, totalN)

	gains = []
	for a in attr:
		gains += totalImportance - calculateRest(D, Y, a, totalP, totalN)
	return idx



def countP_N(Y):
	""" returns a tuple with count of positive and negative """
	p, n = 0,0
	for x in Y:
		if x == 1:
			p += 1
		else:
			n += 1
 
	return (p, n)

def resolveTie(Y):
	(p, n) = countP_N(Y)
	if p >= n:      # if count equals, we decided result to be positive
		return p
	else:
		return n

def isSameClassification(Y):
	''' all examples have the same classification '''
	count = 0
	for x in Y:
		if x == 0:
			count += 1
		elif count != 0:
			break
	if count == 0 or count == len(Y): 
		return True
		
	return False

def DTL(D, Y, attr, p_Y):
	
	if not Y:
		return resolveTie(p_Y) # return PLURALITY-VALUE(parents_example)

	elif isSameClassification(Y):
		return Y[0] # return the classification

	elif len(attr) == 0: # if attributes is empty
		return resolveTie(Y) # return PLURALITY-VALUE(examples)

	# else:
	# 	a = maxGain(examples[0], examples[1], attr)
	
	

def createdecisiontree(D, Y, noise = False):
	
	# is necessary?
	nFeatures = len(D[0])
	nExamples = len(Y)

	# ToDo: testes 21 e 22 enviam true e falses -> int(true) = 1 e int(false) = 0 ???
	ordem=[]


	# feature index list
	attr = [i for i in range(nFeatures)]

	# calculate possible values of all attr
	global attrValues
	for a in attr:
		lst = [] 
		for d_line in D:
			v = d_line[a]
			if v not in lst:
				lst.append(v)
		attrValues.append(lst)
	

	#DTL(D, Y, attr, [])



	return [0,0,1]

D3 = np.array([
			  [0,0,0],
			  [0,0,1],
			  [0,1,0],
			  [0,1,1],
			  [1,0,0],
			  [1,0,1],
			  [1,1,0],
			  [1,1,1]])

Y = np.array([0,1,0,1,0,1,0,1])


if __name__ == '__main__':
	createdecisiontree(D3, Y)