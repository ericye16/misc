#!/usr/bin/env python

from __future__ import division, print_function
from random import normalvariate

k_UsingGaussian = False #very interesting if you make set it True...
k_mu = 11
k_sig = 3
n = 1000

numRetries = 100

if not k_UsingGaussian:
    numRetries = 1

def genK():
    if k_UsingGaussian:
        return int(round(normalvariate(k_mu, k_sig)))
    else:
        return k_mu

    
def factorial(n):
    p = 1
    print("Called factorial!")
    for i in range(1, n + 1):
        p *= i
    return p

def genPascalsTriangle(rows):
    triangle = {}
    for i in range(rows):
        for z in range(i + 1):
            if z == 0:
                triangle[(i, z)] = 1
            elif z == (i):
                triangle[(i, z)] = 1
            else:
                triangle[(i, z)] = (triangle[(i - 1, z - 1)] +
                                    triangle[(i - 1, z)])
    return triangle                

numRows = 1000

pTriangle = genPascalsTriangle(numRows)

def combination(n, k):
    '''N pick k. n is on top. n is larger'''
    if n > numRows:
        return factorial(n)//(factorial(k)*(factorial(n-k)))
    else:
        return pTriangle[(n, k)]

# Defined as: ∑_(x=1)^⌊k/2⌋▒〖((2x-1)¦k)*(d/n)^(2x-1)*(1-d/n)^(k-2x+1) 〗
def getProb(d):
    p = 0
    k = genK()
    for x in range(1, ((k + 1) // 2) + 1):
        #print(x)
        p += combination(k, 2 * x - 1) * ((d / n) ** (2 * x - 1)) * \
             ((1 - (d / n)) ** (k - 2 * x + 1))
    return p

def getData():
    y = []
    for d in range(n):
        z = 0
        for e in range(numRetries):
            z += getProb(d)
            # print(getProb(d))
        z /= numRetries
        y.append(z)
    return y

def plot():
    import matplotlib.pyplot as plt
    plt.plot(range(1, n + 1), getData(), 'r-') #remove 'r-' to make it blue
    plt.show()

def writeToFile(fname):
    import pickle
    fi = open(fname + '.outputs', 'w')
    pickle.dump(getData(), fi, pickle.HIGHEST_PROTOCOL)
    fi.close()



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'write':
        print('Writing to file.')
        if len(sys.argv) > 2:
            fname = sys.argv[2]
        else:
            fname = 'theoreticalCrossings'
        writeToFile(fname)
    else:
        print('Plotting.')
        plot()
