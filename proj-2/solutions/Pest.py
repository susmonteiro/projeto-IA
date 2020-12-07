_debug_ = True

def checkDupBranches(tree):
	idx = tree[0]
	t1 = tree[1]
	t2 = tree[2]
	if isinstance(t1, int) and isinstance(t2, int): # [idx, v1, v2]
		_debug_ and print("both are ints:", tree)
		pass
	elif isinstance(t1, int):	# [idx, v1, [...]]
		t2 = checkDupBranches(t2)
		tree = [idx, t1, t2]
		_debug_ and print("t1 is int:", tree)
	elif isinstance(t2, int):	# [idx, [...], v2]
		t1 = checkDupBranches(t1)
		tree = [idx, t1, t2]
		_debug_ and print("t2 is int:", tree)
	else:	# [idx, [...], [...]]
		t1 = checkDupBranches(tree[1])
		t2 = checkDupBranches(tree[2])
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


# tree = [3, 1, [0, [1, 0, [2, 0, 1]], [1, 1, [2, 0, 1]]]]
# tree = [3, [0, [1, 0, [2, 0, 1]], [1, 1, [2, 0, 1]]], [0, [1, 0, [2, 0, 1]], [1, 1, [2, 0, 1]]]]
tree = [3, [0, [1, 0, [2, 0, 1]], [1, 1, [2, 0, 1]]], [1, 0, [2, 0, 1]]]

print("NOVA:", checkDupBranches(tree))