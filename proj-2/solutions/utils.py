from math import inf

def getSublstMax(lst):
    maxV = -inf
    res = []

    for v in lst:
        if v < maxV:
            continue
        elif v == maxV:
            res.append(v)
        else: ## x > maxV
            maxV = v
            res = [v]

    return res


def getSubdicMax(dic):
    maxV = -inf
    res = []

    for k in dic.keys():
        if dic[k] < maxV:
            continue
        elif dic[k] == maxV:
            res.append(k)
        else: ## x > maxV
            maxV = dic[k]
            res = [k]

    return res


if __name__ == '__main__':
    a= {1:3, 2:4, 3:4, 4:2, 5:4}
    print(getSubdicMax(a))