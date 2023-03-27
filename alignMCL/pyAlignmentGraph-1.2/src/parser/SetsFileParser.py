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
from SetFileParser import *

class SetsFileParser(Parser):
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
		super(SetsFileParser, self).__init__()
		pass

	def process_file(self):
		#self.tempfileparser.reset()
		self.tempfileparser.input(self.input_data)
		self.tempfileparser.parse()
		self.temp = {}
		self.temprowparser = RowParser()
		self.temprowparser.split = True
		self.temprowparser.separator_symbol = '\t'
		self.temprowparser.max_splits = 2
		for i in self.tempfileparser.output_data:
			#print "prova " + i
			self.temprowparser.input(i)
			self.temprowparser.parse()
			#print "prova " + i
			#print self.temprowparser.output_data
			if len(self.temprowparser.output_data) < 2:
				print "Strange line: " + i
				sys.exit()
				continue
			if not self.temprowparser.output_data[0] in self.temp:
				self.temp[self.temprowparser.output_data[0]] = {}
			self.temp[self.temprowparser.output_data[0]][self.temprowparser.output_data[1]] = None
		if len(self.chain) == 0:
			self.output_data = self.temp
			return
		else:
			print "Not yet implemented"
			#self.output_data = self.temp
			sys.exit()
			return
			#self.temp[i] = None
			##self.chain[0].reset()
			#self.chain[0].input(self.files[i])
			#self.chain[0].parse()
			#self.temp[i] = self.chain[0].output_data
		#self.output_data = self.temp
		#self.temp = None

		##print self.temp
		#for i in range(0,len(self.temp)):
			#if self.one_column_listfile_format:
				#key = self.temp[i]
				#value = self.temp[i]
			#elif self.two_columns_listfile_format:
				#if len(self.temp[i]) < 2:
					#print "Wrong list file format. Abort."
					#sys.exit()
				#key = self.temp[i][key_pos]
				#value = self.temp[i][value_pos]
			#self.files[key] = self.prefix + str(value)

	def initialize_output(self):
		self.output_data = {}

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
		self.finalize_output()
