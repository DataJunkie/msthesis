#!/usr/bin/env Python

import sys
import cPickle
import numpy as np
import math

#number of nonzeros (union)
IN = open("nnz.pickle")
nnz = cPickle.load(IN)
IN.close()

for line in sys.stdin:
	row, col, val = line.strip().split(' ')
	j = float(val)/(nnz[int(row)] + nnz[int(col)] - int(val))
	if j < math.pow(10, -4):
		j = 0
	print >> sys.stdout, row, col, str(j)
