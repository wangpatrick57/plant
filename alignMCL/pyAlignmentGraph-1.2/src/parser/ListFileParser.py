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
from NetParser import *
from RowParser import *

class ListFileParser(Parser):
	comment_symbol = None
	column_separator = '\t'
	one_column_listfile_format = True
	two_columns_listfile_format = False
	key_pos = 0
	value_pos = 0
	name_first = True
	use_relative_paths = True
# to maiuscolo 
# header ?

	def __init__(self):
		#print chain
		super(ListFileParser, self).__init__()
		pass

	def process_file(self):
		#self.tempfileparser.reset()
		self.tempfileparser.input(self.input_data)
		self.tempfileparser.parse()
		self.temp = self.tempfileparser.output_data

	def process_files(self):
		#print self.temp
		for i in range(0,len(self.temp)):
			if self.one_column_listfile_format:
				key = self.temp[i]
				value = self.temp[i]
			elif self.two_columns_listfile_format:
				if len(self.temp[i]) < 2:
					print "Wrong list file format. Abort."
					sys.exit()
				key = self.temp[i][key_pos]
				value = self.temp[i][value_pos]
			self.files[key] = self.prefix + str(value)
		#print self.files

	def initialize_output(self):
		self.output_data = {}
		self.files = {}
		if self.use_relative_paths:
			prefix = str(os.path.dirname(self.input_data))
			if not prefix == '':
				prefix = prefix + '/'
		else:
			prefix = ''
		self.prefix = prefix

	def finalize_output(self):
		pass


	def parse(self):
		if self.input_data == None:
			return
		if not type(self.input_data) == str:
			return
		self.initialize_output()
		self.temprowparser = RowParser()
		self.tempfileparser = FileParser()
		self.tempfileparser.set_chain([self.temprowparser])
		self.process_file()
		self.process_files()
		
		if len(self.chain) == 0:
			#print self.files
			self.output_data = self.files
			if len(self.files)==0:
				return
			temp = self.select_format(self.files.keys()[0])
			if not temp == None:
				self.chain.append(temp)
				self.output_data = {}
			else:
				self.output_data = self.files
				return
		self.temp = {}
		for i in self.files:
			self.temp[i] = None
			#self.chain[0].reset()
			self.chain[0].input(self.files[i])
			self.chain[0].parse()
			self.temp[i] = self.chain[0].output_data
		self.output_data = self.temp
		self.temp = None
		
	def select_format(self, input_file):
		temp = os.path.splitext(input_file)
		parser = None
		if temp[1] == '.list':
			print "ListFileParser. List of lists not yet supported."
			sys.exit()
		elif temp[1] == '.nif' or temp[1] == '.sif':
			parser = NetParser()
			parser.set_chain([])
		elif temp[1] == '.txt':
			parser = SetsFileParser()
			parser.set_chain([])
		else:
			print temp[1] + " format unknown."
			sys.exit()
		return parser
