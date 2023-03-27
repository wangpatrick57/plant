#!/pkg/python/2.7.14/bin/python3
# -*- coding: iso-8859-1 -*-
__author__="Marco Mina"
__email__="marco.mina.85@gmail.com"

import sys
import os
from Parser import *

class RowParser(Parser): # rename to StringParser?
	split = False
	separator_symbol = '\t'
	comment_symbol = None
	expected_columns = 0
	max_splits = None

	def __init__(self):
		super(RowParser, self).__init__()
		pass

	def is_ok(self, line):
		if line == '':
			return False
		if not self.comment_symbol == None and line[0] == self.comment_symbol:
			return False
		return True

	def process_line(self, line):
		if self.split:
			if self.max_splits == None:
				line = line.split(self.separator_symbol)
			else:
				line = line.split(self.separator_symbol, self.max_splits)
			if len(line) < self.expected_columns:
				return
			self.output_data = line
		else:
			self.output_data = line
		return

	def finalize_output(self):
		pass
	
	def initialize_output(self):
		self.output_data = None

	def parse(self):
		self.initialize_output()
		#print "This " + self.input_data
		if self.input_data == None:
			return
		if not type(self.input_data) == str:
			return
		line = self.input_data.rstrip('\n')
		line = line.rstrip('\r')
		if not self.is_ok(line):
			#print "Not ok"
			return
		#print "ok" + line
		self.process_line(line)
		self.finalize_output()
