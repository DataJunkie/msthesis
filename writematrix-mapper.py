#!/usr/bin/python

import sys
sys.path.append('.')
from construct_network import * 
import networkx as nx
import jaccard
import scipy.sparse
import numpy as np
import scipy.io

G = BuildGraph()
A = nx.to_scipy_sparse_matrix(G)
intersection_matrix = A * A.transpose()
intersection_matrix = intersection_matrix.tocsr()

nnz = np.load("nnz.pickle.npy").tolist()

for line in sys.stdin:
    row, col = line.strip().split(' ')
    val = imat[int(row), int(col)]
    J = float(val)/(nnz[int(row)] + nnz[int(col)] - int(val))
    if J < math.pow(10, -4):
        J = 0
    if J > 0:
        print >> sys.stdout, row, col, str(J)
