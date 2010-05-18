import sys
import cPickle
import numpy as np
import scipy.sparse
from construct_network import *


#intersection matrix
G = BuildGraph()
A = nx.to_scipy_sparse_matrix(G, dtype="bool")
imat = A.transpose() * A

#number of nonzeros (union)
IN = open("nnz.pickle")
nnz = cPickle.load(IN)
IN.close()

print "Converting to COO. This takes a while. Ugh."
imat = imat.tocoo()
print "Getting nonzero elements."
nonzeros = imat.nonzero()

print "Converting to CSR type."
imat = imat.tocsr()

OUT = open("intersection.mat", "w")
for i in xrange(400000000,len(nonzeros[0])):
	print >> OUT, nonzeros[0][i], nonzeros[1][i], imat[nonzeros[0][i], nonzeros[1][i]]
	if i % 10000000 == 0:
		print i
OUT.close()
