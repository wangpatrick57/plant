#!/pkg/python/2.7.14/bin/python3
# -*- coding: iso-8859-1 -*-
__author__="Marco Mina"
__email__="marco.mina.85@gmail.com"

import sys
import os

#DEFAULT_BREAK_SIMBOL = '\t'
#PARSER_STATUS_INIT = 0
#PARSER_STATUS_PARSING = 1
#PARSER_STATUS_READY = 2

class Parser(object):
	
	def __init__(self):
		self.reset()
		self.chain = []

	def set_chain(self, chain):
		self.chain = chain

	def input(self,data):
		#print "set input data to: " + str(data)
		self.input_data = data
		
	def reset(self):
		self.input_data = None
		self.output_data = None

	def parse(self):
		#print "Generic parser"
		#print self.chain
		next_level_parser = self.chain[0]
		next_level_parser.set_chain(self.chain[1:len(self.chain)])
		#next_level_parser = self.chain[0](self.chain[1:len(self.chain)])
		next_level_parser.input(str(self.input_data))
		next_level_parser.parse()
		self.output_data = next_level_parser.output_data
		#if self.current_status == PARSER_STATUS_INIT:
			#print "Please specify dataset to parse"
		#elif self.current_status == PARSER_STATUS_READY:
			#self.current_status = PARSER_STATUS_PARSING
			#print "Parsing..."
		#elif self.current_status == PARSER_STATUS_PARSING:
			#print "Already parsing another dataset. Please reset current status before parsing other data"
