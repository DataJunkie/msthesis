#!/usr/bin/python

import scipy.sparse
import numpy as np
import scipy.io
import sys

data = np.load("data.pickle.npy")
indices = np.load("indices.pickle.npy")
indptr = np.load("indptr.pickle.npy")
theshape = np.load("shape.pickle.npy")
nnz = np.load("nnz.pickle.npy")

imat = scipy.sparse.csc_matrix((data, indices, indptr), shape=theshape)

for line in sys.stdin:
    row, col = line.strip().split(' ')
    val = imat[row, col]
    J = float(val)/(nnz[int(row)] + nnz[int(col)] - int(val))
    if J < math.pow(10, -4):
        J = 0
    if J > 0:
        print >> sys.stdout, row, col, str(J)
