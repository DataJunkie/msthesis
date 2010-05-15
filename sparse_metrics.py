'''
sparse_metrics.py

Created on April 24, 2010
@author: Ryan R. Rosario
@contact: rosario@stat.ucla.edu
'''
import numpy as np
from scipy.sparse import lil_matrix
import sys
import cProfile
import jaccard

"""
def jaccard(file, lines):
    function jaccard

    PARAMETERS: matrix - incidence or adjacency matrix.
    RETURNS:    matrix of Jaccard values.

    Computes the Jaccard metric for a matrix.
    
    ALGORITHM: 
    Numerator is the number of elements (rowwise) in common.
    Denominator is  
    J = lil_matrix((lines, lines), dtype = 'float')
    IN1 = open(file, "r")
    IN2 = open(file, "r")
    i = j = 0
    for line1 in IN1:
        row1 = line1.strip()
        IN2.seek(0)
        j = 0
        #print i
        for line2 in IN2:
            #print j
            row2 = line2.strip()
            #intersection = str(long(row1, 2) & long(row2, 2)).count('1')
            #union = str(long(row1, 2) | long(row2, 2)).count('1')
            intersection = (bitarray(row1) & bitarray(row2)).count()
            union = (bitarray(row1) | bitarray(row2)).count()
            if union != intersection:
                Jab = float(intersection)/(union - intersection)
                if Jab > 0:
                    J[i, j] = Jab
            j += 1
        #print end - start
        sys.exit()
        i += 1
    return J
"""

def generate_jaccard_components(matrix, ifile, nnzfile, axis=1):
    """
    TO DO:
    1) Add an on-disk parameter to print certain quantities to disk.
    2) Estimate the time required and print to the user.
    """
    try:
        import jaccard
    except:
        raise NotImplementedError

    #Compute the intersection matrix (numerator in Jaccard)
    intersection_matrix = matrix.transpose() * matrix
    #intersection_matrix = intersection_matrix.tocoo()
    #Get the nonzero entries of the intersection matrix.
    data = intersection_matrix.nonzero()
    if axis == 1:
        intersection_matrix = intersection_matrix.tocsc()   #csr?
    elif axis == 2:
        intersection_matrix = intersection_matrix.tocsc()
    else:
        print "Invalid axis specifier."
        sys.exit(-1)
    
    #Print the nonzero entries of the intersection matrix to disk,
    #or keep them in RAM depending on user preference.
    print "Printing nonzero values of intersection matrix  to disk..."
    INTERSECTION = open(ifile, "w")
    #print >> INTERSECTION, ' '.join(["row","col","value"])
    for i in xrange(len(data[0])):
        print >> INTERSECTION, data[0][i], data[1][i], intersection_matrix[data[0][i], data[1][i]]
        INTERSECTION.flush()
    INTERSECTION.close()
    
    #Get the number of non-zero elements in each row (axis = 1) or column (axis = 2)
    #Print the number of nonzeros to disk or keep in RAM depending on user preference.
    print "Printing nonzero counts to disk..."
    m, n = matrix.shape
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
        print "Invalid axis specifier."
        sys.exit(-1)
    NONZEROS.close()
    #Print to disk.

    #Compute Jaccard in R
    r = robjects.r
    nnz = robjects.IntegerVector(nnz)
    robjects.globalEnv["nnz"] = nnz

    return



'''
def logistic(rel,dis,pop,resp):
    try:
        log_fit = r.glm("good~relevance+discrimination+popularity",family="binomial")
    except:
        sys.exit(0)
    return filter(lambda x: x != '',str(log_fit.r['coefficients']).split('\n')[2].split(' ')
'''
