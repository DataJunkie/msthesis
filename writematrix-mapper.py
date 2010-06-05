#!/usr/bin/python

import sys
#sys.path.append('.')
#from construct_network import * 
#import networkx as nx
#import jaccard
import scipy.sparse
import numpy as np
import scipy.io
import math

'''
print >> sys.stderr, "Building graph."
G = BuildGraph()
print >> sys.stderr, "Converting graph to matrix."
A = nx.to_scipy_sparse_matrix(G, dtype="bool")
print >> sys.stderr, "Converting to CSC."
A = A.tocsc()
print >> sys.stderr, "Computing transpose."
intersection_matrix = A * A.transpose()
intersection_matrix = intersection_matrix.tocsr()
'''

#Given the intersection matrix, load it.

indices = np.load("csc-indices.pickle.npy",'r')
indptr = np.load("csc-indptr.pickle.npy",'r')
shape = np.load("csc-shape.pickle.npy",'r')
data = np.load("csc-data.pickle.npy",'r')

imat = scipy.sparse.csr_matrix((data, indices, indptr), shape)

nnz = np.load("nnz.pickle.npy").tolist()

for line in sys.stdin:
    row, col = line.strip().split(' ')
    val = imat[int(row), int(col)]
    J = float(val)/(nnz[int(row)] + nnz[int(col)] - int(val))
    if J < math.pow(10, -4):
        J = 0
    if J > 0:
        print >> sys.stdout, row, col, str(J)
