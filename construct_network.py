import networkx as nx
import re
import sys
import pickle


def BuildGraph():
    IN = open("graph.log", "r")
    nodes = {}
    G = nx.DiGraph()
    for line in IN:
        #read a line and split on comma
        a, b = line.strip().split(',')
        if not nodes.has_key(a):
            G.add_node(a)
        if not nodes.has_key(b):
            G.add_node(b)
        G.add_edge(a, b)
    IN.close()
    return G
        

def main():
    G = BuildGraph()
    print "Nodes/Webpages:      %s" % (G.number_of_nodes(), )
    print "Edges:               %s" % (G.number_of_edges(), )
    print "Writing node order to disk..."
    OUT = open("node_order.dat","w")
    nodes = G.nodes()
    for node in nodes:
        OUT.write(node + '\n')
    OUT.close()
    print "Writing graph to disk..."
    A = nx.to_scipy_sparse_matrix(G)
    C = A.tocsr()
    OUT = open("mygraph.graph","wb")
    pickle.dump(C,OUT,-1)
    OUT.close()

if __name__ == "__main__":
    main()
