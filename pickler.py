from construct_network import *
import jaccard
import cPickle
import numpy as np
import scipy.io

print "Building graph..."
G = BuildGraph()
print "Converting graph to matrix..."
A = nx.to_scipy_sparse_matrix(G, dtype="bool")
#print "Computing transpose..."
intersection_matrix = A * A.transpose()
#print "Converting to CSC type..."
intersection_matrix = intersection_matrix.tocsr()
A = A.tocsr()
#print "Dumping pickle to disk..."
#scipy.io.savemat("intersection.pickle", {'matrix': intersection_matrix})
nnz = jaccard.no_nonzeros(A, axis=1, pickle=True, disk=False, nnzfile="")
print "Done."
