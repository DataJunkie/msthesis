#!/usr/bin/python

import sys
import scipy.sparse
import numpy as np
import scipy.io
import math


indices = np.load("csc-indices.pickle.npy",'r')
indptr = np.load("csc-indptr.pickle.npy",'r')
shape = np.load("csc-shape.pickle.npy",'r')
data = np.load("csc-data.pickle.npy",'r')
print >> sys.stderr, "Loaded matrix."

imat = scipy.sparse.csr_matrix((data, indices, indptr), shape)
print >> sys.stderr, "Created matrix."

nnz = np.load("nnz.pickle.npy",'r')
print >> sys.stderr, "Loaded nnz"

for line in sys.stdin:
    row, col = line.strip().split(' ')
    val = imat[int(row), int(col)]
    J = float(val)/(nnz[int(row)] + nnz[int(col)] - int(val))
    if J < math.pow(10, -4):
        J = 0
    if J > 0:
        print >> sys.stdout, row, col, str(J)
