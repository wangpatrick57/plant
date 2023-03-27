#!/pkg/python/2.7.14/bin/python3
# -*- coding: iso-8859-1 -*-
__author__="Marco Mina"
__email__="marco.mina.85@gmail.com"

import sys
import os
from Parser import *
from NifFileParser import *
from NetParser import *
from igraph import *





class Net(object):
	
	graph = None
	node_attributes = {}
	edge_attributes = {}
	reverse_nodes = {}
	
def load_Net(input_file):
	sfp = NetParser()
	parser = Parser()
	parser.set_chain([sfp])
	parser.input(input_file)
	parser.parse()
	return parser.output_data

def fromigraph(g,invmaps):
	rnet = {}
	edges = g.get_edgelist()
	for i in edges:
		name1 = invmaps[i[0]]
		name2 = invmaps[i[1]]
		if name1 not in rnet:
			rnet[name1] = {}
		rnet[name1][name2] = {}
	return rnet

if __name__ == '__main__':
	
	std_file = [	'test_h.nif',
								'test_f.nif',
								'test_hf.ort'
							]
	#input_file = sys.argv[1]
	
	input_file = std_file[0]
	net1 = load_Net(input_file)
	
	input_file = std_file[1]
	net2 = load_Net(input_file)
	
	input_file = std_file[2]
	ort = load_Net(input_file)
	
	print(str(net1[0]))
	print(str(net2[0]))
	print(str(ort[0]))

	print(type(ort[1]))
	sys.exit()



####
##include <igraph/igraph.h>
        #igraph_i_set_attribute_table(&igraph_cattribute_table);                                                                                          
        #igraph_vector_t x;                                                                                                                               
        #igraph_vector_init(&x, 0);                                                                                                                       
        #igraph_create(graph, &x, 0, 0);                                                                                                                  
        #igraph_vector_destroy(&x);                                                                                                                       
                        #igraph_add_vertices(graph, 1, 0);                                                                                                
                        #igraph_add_vertices(graph, 1, 0);                                                                                                
#//              igraph_add_edge(graph, src, dst);                                                                                                        
        #igraph_vector_t edges;                                                                                                                           
        #igraph_vector_init(&edges,temp_edges_next);
        #for (int i=0; i<igraph_vector_size(&edges); i++) {
        #igraph_add_edges(graph, &edges, 0);
        #printf("edges: %d\n",(int) igraph_ecount(graph));
#int read_graph_edgelist(igraph_t* graph, FILE *in) {
        #igraph_i_set_attribute_table(&igraph_cattribute_table);
        #igraph_vector_t x;
        #igraph_vector_init(&x, 0);
        #igraph_create(graph, &x, 0, 0);
        #igraph_vector_destroy(&x);
                        #igraph_add_vertices(graph, 1, 0);
                        #igraph_add_vertices(graph, 1, 0);
#//              igraph_add_edge(graph, src, dst);
        #igraph_vector_t edges;
        #igraph_vector_init(&edges,temp_edges_next);
        #for (int i=0; i<igraph_vector_size(&edges); i++) {
        #igraph_add_edges(graph, &edges, 0);
        #printf("edges: %d\n",(int) igraph_ecount(graph));

#//      igraph_t graph;
#//      printf("Imported a graph with %d nodes and %d edges\n",(int)igraph_vcount(&graph),(int)igraph_ecount(&graph));
#//      igraph_simplify(&graph, true, true);
#//      printf("Simplified graph: %d nodes and %d edges\n",(int)igraph_vcount(&graph),(int)igraph_ecount(&graph));
