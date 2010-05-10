import networkx as nx
import pickle
from sparse_metrics import generate_jaccard_components

def BuildGraph():
    IN = open("graph.log.1", "r")
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
        

def to_long_list(G, axis=1):
    """Return the graph adjacency matrix as a SciPy sparse matrix.

    Parameters
    ----------
    G : graph
        The NetworkX graph used to construct the list.

    nodelist : list, optional       
       The rows and columns are ordered according to the nodes in `nodelist`.
       If `nodelist` is None, then the ordering is produced by G.nodes().

    dtype : NumPy data-type, optional
        A valid NumPy dtype used to initialize the array. If None, then the
        NumPy default is used.

    Returns
    -------
    M : SciPy sparse matrix
       Graph adjacency matrix.

    Notes
    -----
    The matrix entries are populated using the 'weight' edge attribute. When
    an edge does not have the 'weight' attribute, the value of the entry is 1.
    For multiple edges, the values of the entries are the sums of the edge
    attributes for each edge.

    When `nodelist` does not contain every node in `G`, the matrix is built 
    from the subgraph of `G` that is induced by the nodes in `nodelist`.
    
    Uses lil_matrix format.  To convert to other formats see the documentation
    for scipy.sparse.

    Examples
    --------
    >>> G = nx.MultiDiGraph()
    >>> G.add_edge(0,1,weight=2)
    >>> G.add_edge(1,0)
    >>> G.add_edge(2,2,weight=3)
    >>> G.add_edge(2,2)
    >>> S = nx.to_scipy_sparse_matrix(G, nodelist=[0,1,2])
    >>> S.todense()
    matrix([[ 0.,  2.,  0.],
            [ 1.,  0.,  0.],
            [ 0.,  0.,  4.]])

    """
    nodelist = G.nodes()
    nodeset = set(nodelist)
    if len(nodelist) != len(nodeset):
        msg = "Ambiguous ordering: `nodelist` contained duplicates."
        raise nx.NetworkXError(msg)

    nlen=len(nodelist)
    undirected = not G.is_directed()
    index=dict(zip(nodelist,range(nlen)))
    indices = []
    first_pass = True
    prev_i = 0
    OUT = open("integers.dat", "w")
    for u, v, attrs in G.edges_iter(data=True):
        if (u in nodeset) and (v in nodeset):
            i, j = index[u], index[v]
            if (not first_pass) and (i != prev_i):
                prev_i = i
                indices.sort()
                bitstring = []
                bitstring = ['0' for a in xrange(nlen)]
                for k in indices:
                    bitstring[k] = '1'
                print >> OUT, ''.join(bitstring)
                #print >> OUT,  str(int(''.join(bitstring), 2))
                indices = []
            indices.append(j)
            if first_pass:
                first_pass = False
    OUT.close()
    return


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

    A = nx.to_scipy_sparse_matrix(G, dtype="bool")
    generate_jaccard_components(A, "intersections.mat", "nonzero.mat", axis=1)
    return
    '''
    print "Writing master graph to disk as a sparse matrix..."
    OUT = open("raw.mat", "w")
    pickle.dump(A, OUT, -1)
    OUT.close()

    C = A.tocsr()
    OUT = open("mygraph.mat","wb")
    pickle.dump(C,OUT,-1)
    OUT.close()
    OUT = open("raw.graph", "w")
    pickle.dump(G, OUT, -1)
    OUT.close()

    print jaccard(C) 
    '''

if __name__ == "__main__":
    main()
