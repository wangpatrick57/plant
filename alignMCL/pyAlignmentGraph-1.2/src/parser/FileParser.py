#!/pkg/python/2.7.14/bin/python3
# -*- coding: iso-8859-1 -*-
__author__="Marco Mina"
__email__="marco.mina.85@gmail.com"

import sys
import os
from Parser import *

class FileParser(Parser):
	comment_symbol = None

	def __init__(self):
		#print chain
		super(FileParser, self).__init__()
		pass

	def is_ok(self, line):
		if line == '':
			return False
		if not self.comment_symbol == None and line[0] == self.comment_symbol:
			return False
		return True

	def process_line(self, line):
		self.chain[0].input(line)
		self.chain[0].parse()
		self.output_data.append(self.chain[0].output_data)

	def finalize_output(self):
		pass

	def initialize_output(self):
		self.output_data = []
		if len(self.chain) == 0:
			self.chain.append(RowParser())
			print "No row parser defined. Simply reading lines"

	def parse(self):
		if self.input_data == None:
			return
		if not type(self.input_data) == str:
			return
		self.handle = open(self.input_data,'r')
		self.initialize_output()
		for line in self.handle:
			line = line.rstrip('\n')
			line = line.rstrip('\r')
			if not self.is_ok(line):
				continue
			self.process_line(line)
		self.finalize_output()
		self.handle.close()
		self.handle = None
