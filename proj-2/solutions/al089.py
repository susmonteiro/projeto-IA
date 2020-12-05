# -*- coding: utf-8 -*-
"""
Grupo al089
Duarte Bento #92456
Susana Monteiro #92560
"""
import numpy as np
from math import log
from copy import deepcopy

## GLOBAL

attrValues = []


def importance(p, n):
	if p == 0 or n == 0:
		return 0
	elif p == 1/2:
		return 1
	else:
		posFraction = p/(n+p)
		negFraction = n/(n+p)
		return abs(posFraction*log(posFraction, 2) + negFraction*log(negFraction, 2))

def calculateRest(D, Y, a_idx, totalP, totalN):
	''' Calculate the sum of the rest for a  given attribute '''
	attrVect = attrValues[a_idx]
	rest = 0

	# calculate importance for each value of attr
	for v in attrVect:
		filteredY = []

		# get classification of lines where attr = v
		for idx in range(len(D)):
			if D[idx][a_idx] == v:
				filteredY.append(Y[idx])	
		
		p, n = countP_N(filteredY)
		rest += ((p + n)/(totalP + totalN))*importance(p, n)

	return rest


def maxGain(D, Y, attr):
	""" returns the attribute that resultes in the max gain of information """
	totalP, totalN = countP_N(Y) 
	totalImportance = importance(totalP, totalN)

	gains = dict()
	for a in attr:
		gains[a] = totalImportance - calculateRest(D, Y, a, totalP, totalN)
	
	return max(gains, key=gains.get)



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
		return 1
	else:
		return 0

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
	tmpAttr = deepcopy(attr)

	if len(Y) == 0:
		#print("p_Y: ", p_Y)
		#print("No more examples:", resolveTie(p_Y)) #debug
		return resolveTie(p_Y) # return PLURALITY-VALUE(parents_example)

	elif isSameClassification(Y):
		#print("All have the same classification:", Y) #debug
		return Y[0] # return the classification

	elif len(attr) == 0: # if attributes is empty
		#print("No more attributes:", resolveTie(Y)) #debug
		return resolveTie(Y) # return PLURALITY-VALUE(examples)

	else:
		a = maxGain(D, Y, attr)
		#print("Chosen attribute:", a) #debug

		tree = [a]
		#print(attr, a)
		tmpAttr.remove(a)
		for v in attrValues[a]:
			newD = []
			newY = []
			for i in range(len(D)):
				if D[i][a] == v:
					#newD = np.append(newD, D[i])
					#newY = np.append(newY, Y[i])
					newD.append(D[i])
					newY.append(Y[i])
			#print("newD:", newD) #debug
			#print("newY:", newY) #debug

			subtree = DTL(newD, newY, tmpAttr, Y)
			tree.append(subtree)
		#print(tree)
		return tree
	
	

def createdecisiontree(D, Y, noise = False):
	
	# is necessary?
	nFeatures = len(D[0])
	nExamples = len(Y)
	
	Dlist = [ list(map( int, d_line.tolist())) for d_line in D]
	Ylist = list( map( int, Y.tolist() ) )


	# ToDo: testes 21 e 22 enviam true e falses -> int(true) = 1 e int(false) = 0 ???
	ordem=[]


	# feature index list
	attr = [i for i in range(nFeatures)]

	# calculate possible values of all attr
	global attrValues
	for a in attr:
		lst = [] 
		for d_line in Dlist:
			v = d_line[a]
			if v not in lst:
				lst.append(v)
		lst.sort()
		attrValues.append(lst)

	if nFeatures == 0 or nExamples == 0: # in case there are no features or no examples
		return "Erro de inpuuuuut :))))"
	elif isSameClassification(Ylist):
		return [0, Ylist[0], Ylist[0]]
	else:
		return DTL(Dlist, Ylist, attr, [])



if __name__ == '__main__':
	D20 = np.array([[0, 0, 0],
					[0, 0, 1],
					[0, 1, 0],
					[0, 1, 1],
					[1, 0, 0],
					[1, 0, 1],
					[1, 1, 0],
					[1, 1, 1]])
	Y = np.array([0, 1, 1, 0, 0, 1, 1, 0])

	print(createdecisiontree(D20, Y))