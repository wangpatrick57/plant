#!/pkg/python/2.7.14/bin/python3
# -*- coding: iso-8859-1 -*-

'''
ISSUES: file list saved as a dictionary. Multiple istances of the same file are not allowed!
ISSUES: file list is not ordered!
'''

__author__="Marco Mina"
__email__="marco.mina.85@gmail.com"

import sys
import os
from Parser import *
from FileParser import *
from RowParser import *

class SetFileParser(Parser):
	#comment_symbol = None
	#column_separator = '\t'
	#one_column_listfile_format = True
	#two_columns_listfile_format = False
	#key_pos = 0
	#value_pos = 0
	#name_first = True
	#use_relative_paths = True
# to maiuscolo 
# header ?

	def __init__(self):
		#print chain
		super(SetFileParser, self).__init__()
		pass

	def process_file(self):
		#self.tempfileparser.reset()
		self.next_level_parser.input(self.input_data)
		self.next_level_parser.parse()

	def initialize_output(self):
		self.output_data = {}
		if len(self.chain) == 0:
			self.chain = []
			self.chain.append(RowParser())
		self.next_level_parser = FileParser()
		self.next_level_parser.set_chain(self.chain)

	def finalize_output(self):
		for i in self.next_level_parser.output_data:
			self.output_data[i] = None

	def parse(self):
		if self.input_data == None:
			return
		if not type(self.input_data) == str:
			return
		self.initialize_output()
		self.process_file()
		self.next_level_parser.output_data
		self.finalize_output()
		#print self.output_data