#!/pkg/python/2.7.14/bin/python
# -*- coding: iso-8859-1 -*-
__author__="Marco Mina"
__email__="marco.mina.85@gmail.com"

UNIONGRAPH_INTERNAL_DEBUG = True

import sys
import os
import igraph

import datetime

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

	if UNIONGRAPH_INTERNAL_DEBUG:
		print "Building rev maps"
	r_net1 = build_rev_map(net1)
	r_net2 = build_rev_map(net2)
	r_ort = build_rev_map(ort)

	if UNIONGRAPH_INTERNAL_DEBUG:
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
	
	if UNIONGRAPH_INTERNAL_DEBUG:
		print "Processing net 0 - simple nodes"
	for i in r_net1:
		ri = r_net1[i]
		if not i in r_ort:
			current = len(simple)
			simple.append(i)
			simple_tag.append(1)
			simple_ref.append((ri,None))
			if not ri in reverse_simple[0]:
				reverse_simple[0][ri] = {}
			#if not current in reverse_simple[0][i]:
				reverse_simple[0][ri][current] = None
			else:
				raise Exception

	if UNIONGRAPH_INTERNAL_DEBUG:
		print "Processing net 1 - simple nodes"
	for i in r_net2:
		ri = r_net2[i]
		if not i in r_ort:
			current = len(simple)
			simple.append(i)
			simple_tag.append(2)
			simple_ref.append((None,ri))
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

	if UNIONGRAPH_INTERNAL_DEBUG:
		print "Processing composite nodes"

        bad = 0
	for i in r_ort:
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

			if rrj == None and ri == None: # discard ort node if both the proteins are not in the graph
				continue
			
			#if rrj == None or ri == None: # discard ort node if one of the two proteins is not in the graph
				#continue

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

        
        if UNIONGRAPH_INTERNAL_DEBUG:
                print "Building igraph.Graph"

	g = igraph.Graph(len(composite))
	g.vs['name'] = composite
	g.vs['type'] = composite_tag
	g.vs['ref'] = composite_ref
	#return g
	return build_union_graph_edges(g, net1, net2, ort);
#

def build_union_graph_edges(ug, net1, net2, ort):
        if UNIONGRAPH_INTERNAL_DEBUG:
                print "Entering build_union_graph_edges"
	
	pos = 0
        edge_num = 0
	ci = net1.get_edgelist()

        num_total_edges = 0

        for i in ci:
                num_total_edges += len(reverse_composite[0][i[0]]) * len(reverse_composite[0][i[1]])

	edges = [None] * num_total_edges
	edges_weight = [None] * num_total_edges
	#edges_debug = [None] * num_total_edges
	edges_ref = [None] * num_total_edges

	ss = net1.es['weight']
        total_num = len(ci)
                
	for num, i in enumerate(ci):
                if abs(int(float(num)/total_num * 100.0 ) % 3 - int(float(num-1)/total_num * 100.0 ) % 3) > 1:
			print "Building graph1 edges..." + str(int(float(num)/total_num * 100.0)) + "% completed @ " + str(datetime.datetime.now())
                        
		cs = (ss[pos], None)
		cid = (pos, None)

                all_nodes = set()
                for node1, node2 in ci:
                        all_nodes.add(node1)
                        all_nodes.add(node2)
		for t1 in reverse_composite[0][i[0]]:
			for t2 in reverse_composite[0][i[1]]:
				edges[edge_num] = (t1,t2)
				edges_weight[edge_num] = cs
				edges_ref[edge_num] = cid
                                edge_num += 1
				#print str(net1.vs['name'][i[0]]) + "\t" + str(net1.vs['name'][i[1]]) + "\t" + str(ug.vs['name'][t1]) + "\t" + str(ug.vs['name'][t2])
		pos+=1

	pos = 0
	ci = net2.get_edgelist()
	ss = net2.es['weight']

	for i in ci:
                if abs(int(float(num)/total_num * 100.0 ) % 3 - int(float(num-1)/total_num * 100.0 ) % 3) > 1:
			print "Building graph2 edges..." + str(int(float(num)/total_num * 100.0)) + "% completed"
                
		cs = (None, ss[pos])
		cid = (None, pos)
		for t1 in reverse_composite[1][i[0]]:
			for t2 in reverse_composite[1][i[1]]:
				edges.append((t1,t2))
				edges_weight.append(cs)
				edges_ref.append(cid)
		pos+=1

	ug.add_edges(edges)
	ug.es['weight'] = edges_weight
	ug.es['ref'] = edges_ref
	#ug.es['debug'] = edges_debug
	return merge_union_graph_edges(ug)
#

def merge_union_graph_edges(og): # extend to many networks!
	if UNIONGRAPH_INTERNAL_DEBUG:
		print "Merging conserved edges"
	#g = og.copy() # should not be necessary!
	g = og
	is_mult = g.is_multiple()
	edgeset = g.get_edgelist()
	edgescore = g.es['weight']
	edgeref = g.es['ref']
	n_mult = 0
	
	tomerge = []
	todel = []
	
	for i in range(0,len(is_mult)):
			if is_mult[i]:
					n_mult+=1
					#if not i == g.get_eid(edgeset[i][0], edgeset[i][1]):
					tomerge.append((edgeset[i][0], edgeset[i][1], edgescore[i], edgeref[i]))
					todel.append(i)
					#print str(edgeset[i]) + "\t" + str(i) + "\t" + str(g.get_eid(edgeset[i][0], edgeset[i][1]))
	g.delete_edges(todel)
	
	edgeset = g.get_edgelist()
	edgescore = g.es['weight']
	edgeref = g.es['ref']
	
	for i in range(0,len(tomerge)):
		cr = tomerge[i]
		ta = g.get_eid(cr[0], cr[1])
		cs = edgescore[ta]
		cref = edgeref[ta]
		ncs = []
		ncr = []
		for i in range(0,len(cs)):
			if(cs[i] == None):
				ncs.append(cr[2][i])
				ncr.append(cr[3][i])
			elif(cr[2][i] == None):
				ncs.append(cs[i])
				ncr.append(cref[i])
			else:
				raise Exception
		ncs = tuple(ncs)
		ncr = tuple(ncr)
		edgescore[ta] = ncs
		edgeref[ta] = ncr

	g.es['weight'] = edgescore
	g.es['ref'] = edgeref

	return g
#

