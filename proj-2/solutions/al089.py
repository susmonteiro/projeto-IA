# -*- coding: utf-8 -*-
"""
Grupo al089
Duarte Bento #92456
Susana Monteiro #92560
"""
import numpy as np
from math import log, inf
from copy import deepcopy
from itertools import permutations	
from random import randint, seed
from time import time
# import datasetstreelearning

seed(time())

## GLOBAL
_debug_ =  False

K = 10
EMPTY_TREE = 2
attrValues = []


###
###		Create Decision Tree
###

def createdecisiontree(D, Y, noise = False):
	""" Creates the decision tree, wehther with or without noise """
	nFeatures = len(D[0])
	nExamples = len(Y)

	Dlist = [ list(map( int, d_line.tolist())) for d_line in D]
	Ylist = list(map(int, Y.tolist()))

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
		return -1
	elif isSameClassification(Ylist):
		return [0, Ylist[0], Ylist[0]]
	elif noise == False:
		dtl = DTL(Dlist, Ylist, attr, [], perm=True)
		return removeDupBranches(dtl)
	else: # if there's noise
		dtl = DTLnoise(Dlist, Ylist, K, attr, nExamples)
		return removeDupBranches(dtl)
		

def removeDupBranches(tree):
	""" Recursive function thar given a dtl, returns an equivalent dtl with no unnecessary repeated branches """
	idx = tree[0]
	t1 = tree[1]
	t2 = tree[2]
	if isinstance(t1, int) and isinstance(t2, int): # [idx, v1, v2]
		_debug_ and print("both are ints:", tree)
		pass
	elif isinstance(t1, int):	# [idx, v1, [...]]
		t2 = removeDupBranches(t2)
		tree = [idx, t1, t2]
		_debug_ and print("t1 is int:", tree)
	elif isinstance(t2, int):	# [idx, [...], v2]
		t1 = removeDupBranches(t1)
		tree = [idx, t1, t2]
		_debug_ and print("t2 is int:", tree)
	else:	# [idx, [...], [...]]
		t1 = removeDupBranches(tree[1])
		t2 = removeDupBranches(tree[2])
		if t1[0] != t2[0]: # there are no repeated branches
			pass
		elif t1[1] == t2[1] and t1[2] == t2[2]:
			tree = t1		# remove root node
		elif t1[1] == t2[1]: # negative branches are duplicated
			_debug_ and print("negative branches duplicated")
			tree[0] = t1[0]
			tree[1] = t1[1] # == tree[1] = t2[1]
			tree[2][0] = idx
			tree[2][1] = t1[2]
			_debug_ and print(tree)
		elif t1[2] == t2[2]: # positive branches are duplicated
			_debug_ and print("positive branches duplicated")
			tree[0] = t1[0]
			tree[2] = t1[2]
			tree[1][0] = idx
			tree[1][2] = t2[1]
			_debug_ and print(tree)
	return tree


###
###		Tree Learning Algorithm (general)
###

def DTL(D, Y, attr, p_Y, perm=False):
	""" Recursive function that given a set of examples and results, returns a decision tree """
	if len(Y) == 0:
		_debug_ and print("No more examples:", resolveTie(p_Y))
		return resolveTie(p_Y) # return PLURALITY-VALUE(parents_example)

	elif isSameClassification(Y):
		_debug_ and print("All have the same classification:", Y)
		return Y[0] # return the classification

	elif len(attr) == 0: # if attributes is empty
		_debug_ and print("No more attributes:", resolveTie(Y))
		return resolveTie(Y) # return PLURALITY-VALUE(examples)

	else:
		attrLst = maxGain(D, Y, attr)
		_debug_ and print("Chosen attributes:", attrLst)

		if perm:
			# get all permutations of attributes with max gain
			matrixAttr = list(permutations(attrLst))
		else:
			matrixAttr = [[attrLst[-1]]]	# only the first attribute that maximizes gain
				
		tree = []					# final (local) best tree	
		for aList in matrixAttr:	# loop through [[a1,(a2,...)],([a1,(a2,...)]...)]
			tmpTree = []

			for a in aList:			# loop through [a1,(a2,...)]

				tmp2Tree = [a]		# tree (local) root index 
				tmpAttr = deepcopy(attr)
				tmpAttr.remove(a)	# subtracts A from main list of attributes


				for v in attrValues[a]:	# loop through [v1, v2, ...] (column of attribute a)
					newD = []
					newY = []
					for i in range(len(D)):
						if D[i][a] == v:
							newD.append(D[i])
							newY.append(Y[i])

					_debug_ and print("newD:", newD) 
					_debug_ and print("newY:", newY)

					subtree = DTL(newD, newY, tmpAttr, Y, perm)	# propagates perm decision
					tmp2Tree.append(subtree)
			
				# for one list attribute
				if len(str(tmpTree)) == EMPTY_TREE or len(str(tmp2Tree)) < len(str(tmpTree)):
					# shorter tree, update
					tmpTree = deepcopy(tmp2Tree)
			
			# for all permutations
			if len(str(tree)) == EMPTY_TREE or len(str(tmpTree)) < len(str(tree)):
					# shorter tree, update
					tree = deepcopy(tmpTree)

		return tree


def maxGain(D, Y, attr):
	""" Returns the attribute that resultes in the max gain of information """
	totalP, totalN = countP_N(Y) 
	totalImportance = importance(totalP, totalN)

	gains = dict()
	for a in attr:
		gains[a] = totalImportance - calculateRest(D, Y, a, totalP, totalN)
		_debug_ and print("attr:", a, "gain:", gains[a])
	
	return getSubdicMax(gains)


def resolveTie(Y):
	""" Returns value to assign when there is a tie """
	(p, n) = countP_N(Y)
	if p >= n:      # if count equals, we decided result to be positive
		return 1
	else:
		return 0

def isSameClassification(Y):
	""" Check if all examples have the same classification """
	count = 0
	for x in Y:
		if x == 0:
			count += 1
		elif count != 0:
			break
	if count == 0 or count == len(Y): 
		return True
		
	return False



###
###		Tree Learning Algorithm (WITH noise)
###

def DTLnoise(D, Y, K, attr, nExamples, perm=True):
	""" Generates a decision tree that scores best (lowest error) """
	minTree = []
	minErr = inf
	for _ in range(K):
		trainD, trainY, testD, testY = getNoiseSets(D, Y, K, nExamples)
		tree = DTL(trainD, trainY, attr, [], perm)
		_debug_ and print(tree)
		tryY = noiseClassify(tree, testD)
		_debug_ and print(testY)
		_debug_ and print(tryY)
		err = np.mean(np.abs(np.array(testY)-tryY))
		if (err < minErr):
			minTree = deepcopy(tree)
			minErr = err
		_debug_ and  print(err)
	return minTree


def getNoiseSets(D, Y, K, nExamples):
	""" Generates sets to train for noise.
	Randomly choose 1/k of the data set to be tests\
	and (k-1)/k examples for learning """
	random_idxs = []	# set of random indexes to be part of the test set
	
	for i in range(nExamples//K): # fill random_idxs
		rn = randint(0, nExamples-1)
		while rn in random_idxs:
			rn = randint(0, nExamples-1)
		random_idxs.append(rn)

	_debug_ and print(random_idxs)
	_debug_ and print(nExamples//K, len(random_idxs))

	trainD = deepcopy(D)
	trainY = deepcopy(Y)
	testD = []
	testY = []

	for i in range(nExamples-1, -1, -1):
		if i in random_idxs:
			testD.append(trainD.pop(i))
			testY.append(trainY.pop(i))
			random_idxs.remove(i)

	_debug_ and print("trainD", trainD) 
	_debug_ and print("testD", testD)
	_debug_ and print("trainY", trainY)
	_debug_ and print("testY", testY)

	return trainD, trainY, testD, testY


def noiseClassify(T,data):
	""" Returns the result of apply the tree T to the data.
	Obtained from 'testdecicionstree.py' """

	data = np.array(data)
	out = []
	for el in data:
		wT = T
		for ii in range(len(el)):
			if el[wT[0]]==0:
				if isinstance(wT[1],int):
					out += [wT[1]]
					break
				else:
					wT = wT[1]
			else:
				if isinstance(wT[2],int):
					out += [wT[2]]
					break
				else:
					wT = wT[2]
	return np.array(out)




###
###		Utils
###

def getSubdicMax(dic):
	""" Returns a subDictionary with all values that match max """
	maxV = -inf
	res = []

	for k in dic.keys():
		if dic[k] < maxV:
			continue
		elif dic[k] == maxV:
			res.append(k)
		else: # x > maxV
			maxV = dic[k]
			res = [k]

	return res


def importance(p, n):
	""" Calculate the importance (entropy) """
	if p == 0 or n == 0:
		return 0
	elif p == 1/2:
		return 1
	else:
		posFraction = p/(n+p)
		negFraction = n/(n+p)
		return abs(posFraction*log(posFraction, 2) + negFraction*log(negFraction, 2))


def calculateRest(D, Y, a_idx, totalP, totalN):
	""" Calculate the sum of the rest for a  given attribute """
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


def countP_N(Y):
	""" Returns a tuple with count of positive and negative """
	p, n = 0,0
	for x in Y:
		if x == 1:
			p += 1
		else:
			n += 1
	return (p, n)




if __name__ == '__main__':

	# global _debug_
	_debug_ = True

	# D,Y, _, __= datasetstreelearning.dataset(22)

	# print("len D:", len(D[0]), "D:", D)
	# print("len Y:", len(Y), "Y:", Y)
	# print(createdecisiontree(D,Y, noise=True))