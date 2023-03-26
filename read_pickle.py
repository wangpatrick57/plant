#!/bin/python3
import sys
import pickle

file_name = sys.argv[1]

with (open(file_name, "rb")) as f:
    obj = pickle.load(f, encoding='latin1')
    print(obj)
    print(type(obj))
