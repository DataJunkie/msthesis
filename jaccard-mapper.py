#!/usr/bin/python

import sys
import cPickle
import numpy as np
import math

#number of nonzeros (union)
nnz = np.load("nnz.pickle.npy")

for line in sys.stdin:
    try:
	    row, col, val = line.strip().split(' ')
    except:
        continue
    j = float(val)/(nnz[int(row)] + nnz[int(col)] - int(val))
    if j < math.pow(10, -4):
		j = 0
    if j > 0:
        print >> sys.stdout, row, col, str(j)
