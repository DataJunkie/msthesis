from construct_network import *
import networkx as nx
import time
import sys

G = BuildGraph()
el = nx.to_edgelist(G)
names = {}
numbers = {}
i = 0
edgelist = []
for e in el:
    for j in [0,1]:
        if not numbers.has_key(e[j]):
            numbers[e[j]] = i
            names[i] = e[j]
            i += 1
    edgelist.append((numbers[e[0]], numbers[e[1]]))

el = []


#Construct A and A'
start = time.time()
A = {}; Aprime = {}; nnz = [0]*len(numbers)
for e in edgelist:
    if A.has_key(e[0]):
        A[e[0]].update([e[1]])
    else:
        A[e[0]] = set([e[1]])
    if Aprime.has_key(e[1]):
        Aprime[e[1]].update([e[0]])
    else:
        Aprime[e[1]] = set([e[0]])
    nnz[e[0]] += 1

edgelist = []
end = time.time()
print end-start

Aprime = {}
cPickle.dump(open("names.mat","w"), names)
cPickle.dump(open("numbers.mat","w"), numbers)
names = {}; numbers = {}
print "Computing AA'"
product = {}
for i in A:
    for j in A:
        #start = time.time()
	if not product.has_key((j,i)):
		if i == j:
			product[(i,i)] = len(A[i])
		else:
        		product[(i,j)] = len(A[i].intersection(A[j]))
	else:
		pass
        #end = time.time()
        #print end-start
        #sys.exit(0)
print "Saving matrix to disk..."
cPickle.dump(open("intersection-100.mat","w"), product)
'''
1 0 1
0 1 0
1 1 0
'''
'''
A = {}
A[0] = set([0, 2])
A[1] = set([1])
A[2] = set([0, 1])

Aprime = {}
Aprime[0] = set([0, 2])
Aprime[1] = set([1, 2])
Aprime[2] = set([0])

product = {}
print "c(",
for i in A:
    for j in A: #transpose
        start = time.time()
	if i == j:
		product[(i,i)] = len(A[i])
	else:
        	product[(i,j)] = len(A[i].intersection(A[j])) #transpose
        end = time.time()
        print str(end-start), ',',
print ")",

print zip(product.keys(), product.values())
'''
