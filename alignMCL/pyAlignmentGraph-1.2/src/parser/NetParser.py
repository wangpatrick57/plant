#!/pkg/python/2.7.14/bin/python3
# -*- coding: iso-8859-1 -*-

'''
ISSUES: only nodes are saved, not the whole network

'''

__author__="Marco Mina"
__email__="marco.mina.85@gmail.com"

import sys
import os
from Parser import *
from FileParser import *
from NifFileParser import *
from PlainNetFileParser import *
from SifFileParser import *
from RowParser import *
import igraph

class NetParser(Parser):

	def __init__(self):
		super(NetParser, self).__init__()
		self.output_nodes_only = False
		self.output_edges_only = False
		self.output_igraph_only = True

	def _process_file(self):
		self.next_level_parser.input(self.input_data)
		self.next_level_parser.parse()

	def _initialize(self):
		self.output_data = {}
		if self.chain == None or len(self.chain)==0:
			self.chain = []
			input_file = self.input_data
			temp = os.path.splitext(input_file)
			if str(temp[1]) == '.nif':
				self.chain.append(NifFileParser())
			elif str(temp[1]) == '.sif':
				self.chain.append(SifFileParser())
			elif str(temp[1]) == '.ort':
				self.chain.append(PlainNetFileParser())
			else:
				print "NetParser warning: " + temp[1] + " format unknown."
				sys.exit()
		self.next_level_parser = self.chain[0]
		self.next_level_parser.set_chain(self.chain[1:len(self.chain)])

	def _finalize_output(self):
		if self.output_nodes_only:
			self.output_data = self.next_level_parser.output_data[0]
		elif self.output_edges_only:
			self.output_data = self.next_level_parser.output_data[1]
		else:
			maps={}
			invmaps=[]
			num=0
			for i in self.next_level_parser.output_data[0]:
				maps[i] = num
				invmaps.append(i)
				num = num + 1
			g = igraph.Graph(len(maps))
			edgetuple = []
			edgescores = []
			for i in self.next_level_parser.output_data[1]:
				n1 = maps[i]
				for j in self.next_level_parser.output_data[1][i]:
					n2 = maps[j]
					edgetuple.append((n1,n2))
					edgescores.append(self.next_level_parser.output_data[1][i][j])
			g.add_edges(edgetuple)
			g.vs['name'] = invmaps
			g.es['weight'] = edgescores
			
			if self.output_igraph_only:
				self.output_data = [g, invmaps]
			else:
				self.output_data = [self.next_level_parser.output_data[0], self.next_level_parser.output_data[1], g, invmaps]

	def parse(self):
		if self.input_data == None:
			return
		if not type(self.input_data) == str:
			return
		self._initialize()
		self._process_file()
		self._finalize_output()
		#print self.output_data
