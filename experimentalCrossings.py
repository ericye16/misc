#!/usr/bin/env python

# Creds to Andrew who first wrote it.

from __future__ import division, print_function
import matplotlib.pyplot as plt
from random import gauss,randrange

k_UsingGaussian = True
k_mu = 11
k_sig = 3

n = 1000
allele1 = 0
numberOfTimesToRunSims = 100

#instead of representing chromosomes as lists of capital/small letters, split it
#into lists of numbers between 0 and n-1, and n and 2n-1.
A1 = range(n)
A2 = range(n, 2 * n)

def k():
    if k_UsingGaussian:
        return int(round(gauss(k_mu, k_sig)))
    else:
        return k_mu

#int(round(gauss(3,3)+0.5))+1
def crossOver(chromosome1,chromosome2):
    for i in range(k()):
        cut = randrange(1, n)
        old1 = chromosome1[:]
        old2 = chromosome2[:]
        chromosome1 = old1[:cut] + old2[cut:]
        chromosome2 = old2[:cut] + old1[cut:]
    return chromosome1


def isOnSameChromosome(allele1, allele2, chrome):
    if allele1 in chrome and allele2 in chrome:
        return True
    elif allele1 not in chrome and allele2 not in chrome:
        return True
    else:
        return False

def runSims(num, chrome1, chrome2, allele1, allele2):
    numCrosses = 0
    for i in range(num):
        if not isOnSameChromosome(allele1, allele2, crossOver(chrome1[:], chrome2[:])):
            numCrosses += 1
    return numCrosses

def fdisplay():
    hits = []
    for i in range(1, n):
        hits.append(runSims(numberOfTimesToRunSims, A1, A2, allele1, i))
    y = []
    for i in range(n - 1):
        y.append(hits[i]/numberOfTimesToRunSims)
    plt.plot(range(n - 1), y)
    plt.show()

if __name__ == '__main__':
    fdisplay()
