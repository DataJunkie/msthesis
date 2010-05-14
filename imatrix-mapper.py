#!/usr/bin/env Python

import sys
import cPickle
import numpy as np

IN = open("intersection.pickle")
imat = cPickle.load(IN)
IN.close()
for line in sys.stdin:
    for i in xrange(len(nonzeros[0])):
        print >> sys.stdout, nonzeros[0][i], nonzeros[1][i], imat[nonzeros[0][i], nonzeros[1][i]]
