from construct_network import BuildGraph
import networkx as nx
import time
import sys
import cPickle
from itertools import combinations

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


cPickle.dump(names, open("names.mat","w"))
cPickle.dump(numbers, open("numbers.mat","w"))


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

cPickle.dump(A, open("A.pickle","w"))
sys.exit(0)

edgelist = []
end = time.time()
print end-start

Aprime = {}
names = {}; numbers = {}

A = cPickle.load(open("A.pickle"))
product = {}
print len(A.keys())

'''
OUT = open("output.out","w")
j = 0
start = time.time()
for i in combinations(A, 2):
	print >> OUT, i[0], i[1], len(A[i[0]] & A[i[1]])
	#print j
	if j % 10000000 == 0:
		print i
		end = time.time()
		print str(end-start)
		start = time.time()
	j += 1
	#print str(end-start)
'''


'''
row = 0
for i in A.iterkeys():
    start = time.time()
    for j in A.iterkeys():
        #start = time.time()
	if not (j,i) in A:
		if i == j:
			product[(i,i)] = len(A[i])
		else:
        		product[(i,j)] = len(A[i].intersection(A[j]))
	else:
		pass
        #end = time.time()
        #print end-start
        #sys.exit(0)
    row += 1
    end = time.time()
    print "Row: ", str(row), str(end-start)
    sys.exit(0)
print "Saving matrix to disk..."
cPickle.dump(product, open("intersection-100.mat","w"))
'''



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
