'''
jaccard.py

Created on May 10, 2010
@author: Ryan R. Rosario
@contact: rosario@stat.ucla.edu
'''
import sys
import time
import cPickle
import numpy as np

class InvalidArgumentError(Exception):
    def __init__(self, msg):
        self.msg = msg


def imatrix(matrix, axis=1):
    #Compute the intersection matrix (numerator in Jaccard)
    intersection_matrix = matrix.transpose() * matrix
    return intersection_matrix


def numerator(matrix, axis=1):
    #The numerator is always printed to disk.
    return imatrix(matrix, axis)


def output_intersection_matrix(imat, ifile, axis=1, disk=True): 
    #intersection_matrix = intersection_matrix.tocoo()
    #Get the nonzero entries of the intersection matrix.
    print "WARNING: For large matrices, this process takes a long time."
    nonzeros = imat.nonzero()
    if axis == 1:
        imat = imat.tocsc()   #csr?
    elif axis == 2:
        imat = imat.tocsc()
    else:
        raise InvalidArgumentError("Invalid axis specifier.")
    #Print the nonzero entries of the intersection matrix to disk,
    #or keep them in RAM depending on user preference.
    print "Printing nonzero values of intersection matrix to disk..."
    INTERSECTION = open(ifile, "w")
    start = time.time()
    for i in xrange(len(nonzeros[0])):
        print >> INTERSECTION, nonzeros[0][i], nonzeros[1][i], imat[nonzeros[0][i], nonzeros[1][i]]
        if (i % 1000 == 0) and (i > 0) == 0:
            INTERSECTION.flush()
            if (i == 1000):
                end = time.time()
                eta = (((end-start) / 1000) * len(nonzeros))/3600
                print "Estimated time to completion is %f hours." % eta 
    INTERSECTION.close()
    return


def no_nonzeros(matrix, axis=1, pickle=True, disk=False, nnzfile=""):
    #et the number of non-zero elements in each row (axis = 1) or column (axis = 2)
    #Print the number of nonzeros to disk or keep in RAM depending on user preference.
    print type(matrix)
    print "Axis: ", axis
    print "Pickle: ", pickle
    print "Disk: ", disk
    print "File: ", nnzfile
    print "Printing nonzero counts to disk..."
    m, n = matrix.shape
    if disk:
        NONZEROS = open(nnzfile, "w")
        if axis == 1:
            for i in xrange(n):
                print >> NONZEROS, matrix[i,:].nnz
                if i % 1000 == 0:
                    NONZEROS.flush()
                    print i
        elif axis == 2:
            for i in xrange(n):
                print >> NONZEROS, matrix[:,i].nnz
                if i % 1000 == 0:
                    NONZEROS.flush()
                    print i
        else:
            raise InvalidArgumentError("Invalid axis specifier.")
        NONZEROS.close()
        return True
    else:
        print "Will not be printed to ASCII file."
        if axis == 1:
            nnz = [matrix[i,:].nnz for i in xrange(n)]
        elif axis == 2:
            nnz = [matrix[:,i].nnz for i in xrange(n)]
        else:
            raise InvalidArgumentError("Invalid axis specifier.")
	if pickle:
		PICKLE = open("nonzeros.pickle", "w")
		np.save("nonzeros.pickle", nnz)
		PICKLE.close()
	else:
        	return nnz
    return False


def compute(incmatrix, matrixfile, nnzfile, axis=1, ondisk=True):
    #Compute intersection matrix and number of nonzeros in it.
    #Then, write it to disk for use in R to compute the denominator.
    imatrix = numerator(incmatrix, filename, axis) #name is misleading
    #print intersection matrix to disk, if user chooses to.
    output_intersection_matrix(imatrix, axis, matrixfile)
    #print nonzeros to disk, if user chooses to
    result = no_nonzeros(incmatrix, axis, ondisk, nnzfile)
    assert(result == True or len(result) > 0)
    return
