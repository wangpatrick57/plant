#!/pkg/python/2.7.14/bin/python3
# -*- coding: iso-8859-1 -*-
__author__="Marco Mina"
__email__="marco.mina.85@gmail.com"

import sys
import os
#from ListFile import *
from Parser import *
#from ListFileParser import *
from RowParser import *
#from SetFileParser import *
#from SetsFileParser import *
from NifFileParser import *
from NetParser import *
import igraph

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

def build_rev_map(graph):
	a = {}
	na = graph.vs['name']
	for i in range(0,len(na)):
		a[na[i]] = i
	return a
#

def build_map(graph):
	a = {}
	na = graph.vs['name']
	for i in range(0,len(na)):
		a[i] = na[i]
	return a
#

def build_union_graph(net1, net2, ort):
	global r_net1, r_net2, r_ort, m_net1, m_net2, m_ort, reverse_composite

	print "Building rev maps"
	r_net1 = build_rev_map(net1)
	r_net2 = build_rev_map(net2)
	r_ort = build_rev_map(ort)

	print "Building maps"
	m_net1 = build_map(net1)
	m_net2 = build_map(net2)
	m_ort = build_map(ort)
	
	simple = []
	simple_tag = []
	simple_ref = []
	reverse_simple = []
	reverse_simple.append({})
	reverse_simple.append({})
	
	print "Processing net 0 - simple nodes"
	for i in r_net1:
		ri = r_net1[i]
		if not i in r_ort:
			current = len(simple)
			simple.append(i)
			simple_tag.append(1)
			simple_ref.append(None)
			if not ri in reverse_simple[0]:
				reverse_simple[0][ri] = {}
			#if not current in reverse_simple[0][i]:
				reverse_simple[0][ri][current] = None
			else:
				raise Exception

	print "Processing net 1 - simple nodes"
	for i in r_net2:
		ri = r_net2[i]
		if not i in r_ort:
			current = len(simple)
			simple.append(i)
			simple_tag.append(2)
			simple_ref.append(None)
			if not ri in reverse_simple[1]:
				reverse_simple[1][ri] = {}
			#if not current in reverse_simple[0][i]:
				reverse_simple[1][ri][current] = None
			else:
				raise Exception
	
	composite = simple
	composite_tag = simple_tag
	reverse_composite = reverse_simple
	composite_ref = simple_ref

	print "Processing composite nodes"
	for i in r_ort:
		#print "--"
		#print i
		if i in r_net1:
			#print "ort"
			#print ri
			#print r_ort[i]
			#print m_ort[r_ort[i]]
			if not m_ort[r_ort[i]] == i:
				raise Exception
			ri = r_net1[i]
			if not net1.vs['name'][ri] == i:
				raise Exception
		else:
			ri = None

		neigh = ort.neighbors(r_ort[i])
		

		for j in neigh:
			#print j
			rj = m_ort[j]
			#print rj

			current = len(composite)
			if rj in r_net2:
				rrj = r_net2[rj]
				if not net2.vs['name'][rrj] == rj:
					raise Exception
			else:
				rrj = None

			composite.append(i +'/'+ rj)
			composite_tag.append(0)
			composite_ref.append((ri,rrj))
			
			if not ri == None:
				if not i in reverse_composite[0]:
					reverse_composite[0][ri] = {}
				if not current in reverse_composite[0][ri]:
					reverse_composite[0][ri][current] = None
			if not rrj == None:
				if not rrj in reverse_composite[1]:
					reverse_composite[1][rrj] = {}
				if not current in reverse_composite[1][rrj]:
					reverse_composite[1][rrj][current] = None

	g = igraph.Graph(len(composite))
	g.vs['name'] = composite
	g.vs['type'] = composite_tag
	g.vs['ref'] = composite_ref
	#return g
	return build_union_graph_edges(g, net1, net2, ort);
#

def build_union_graph_edges(ug, net1, net2, ort):
	edges = []
	edges_weight = []
	#edges_debug = []

	pos = 0
	ci = net1.get_edgelist()
	ss = net1.es['weight']
	for i in ci:
		cs = ss[pos]
		for t1 in reverse_composite[0][i[0]]:
			for t2 in reverse_composite[0][i[1]]:
				edges.append((t1,t2))
				edges_weight.append(cs)
				#print str(net1.vs['name'][i[0]]) + "\t" + str(net1.vs['name'][i[1]]) + "\t" + str(ug.vs['name'][t1]) + "\t" + str(ug.vs['name'][t2])
		pos+=1

	pos = 0
	ci = net2.get_edgelist()
	ss = net2.es['weight']
	for i in ci:
		cs = ss[pos]
		for t1 in reverse_composite[1][i[0]]:
			for t2 in reverse_composite[1][i[1]]:
				edges.append((t1,t2))
				edges_weight.append(cs)
		pos+=1

	ug.add_edges(edges)
	ug.es['weight'] = edges_weight
	#ug.es['debug'] = edges_debug
	return ug
#


def go():
	global net1, net2, ort

	std_file = [	'test_h.nif',
								'test_y.nif',
								'test_hy.ort'
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
	
	union_graph = build_union_graph(net1[0],net2[0],ort[0])
	return union_graph

def write_graph(g, f):
	h = open(f,'w')
	ge = g.get_edgelist()
	vn = g.vs['name']
	es = g.es['weight']
	pos = 0
	for i in ge:
		#print i
		h.write(str(vn[i[0]]) + "\t" + 
						str(vn[i[1]]) + "\t" + 
						str(es[pos]) + "\n")
		pos+=1
	h.close()
#


if __name__ == '__main__':
	go()
	print(type(ort[1]))
	sys.exit()
