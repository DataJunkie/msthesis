'''
sparse_metrics.py

Created on April 24, 2010
@author: Ryan R. Rosario
@contact: rosario@stat.ucla.edu
'''
import numpy as np


def jaccard(matrix):
    """
    function jaccard

    PARAMETERS: matrix - incidence or adjacency matrix.
    RETURNS:    matrix of Jaccard values.

    Computes the Jaccard metric for a matrix.
    
    ALGORITHM: 
    Numerator is the number of elements (rowwise) in common.
    Denominator is  
    """
    A = matrix.tolil()
    row1 = A[1,:].toarray()
    row2 = A[2,:].toarray()
    numerator = np.bitwise_and(row1, row2)
    C[1:].sum(axis=1)

