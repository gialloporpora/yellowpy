from __future__ import division
from collections import OrderedDict
import sys
import re
import os
from os.path import getmtime, getctime



def bestsize(filepath):
	""" Return a tuple with 3 values. The first is the file (or folder size). The second and thid
	have sense only for folder and are the number of files and subdirectories in folder
	"""
	from os.path import getsize, isdir
	if not(isdir(filepath)): return (getsize(filepath), 1, 0)
	else:
		lf = []
		ld = []
		for root, dirs, files in os.walk(filepath):
			for name in files: lf.append(os.path.join(root, name))
			for dir in dirs: ld.append(os.path.join(root, dir))
		return (sum(getsize(i) for i in lf), len(lf), len(ld))
		
def smartSize(size, unit=None):
	if not(unit):
		unit = 0
		while (size//1024**(unit+1)>0):
			unit = unit + 1
	units = ["B", "KB", "MB", "GB", "TB"]
	if isinstance(unit, str): unit = units.index(unit.upper())
	if unit==0: return "%s Bytes" %size
	else: return "{:6.2f} {unit}".format(size/1024**unit, unit = units[unit])

class gFile(OrderedDict):
	def __init__(self, filepath):
		super(gFile, self).__init__({})
		if os.path.exists(filepath):
			self["filename"] = os.path.basename(filepath)
			self["relpath"]  = os.path.dirname(filepath)
			self["ext"] = os.path.splitext(filepath)[-1]
			self["path"] = os.path.abspath(filepath)
			if os.path.isdir(filepath): 
				self["type"] = "D"
				(self["size"], self["filecount"], self["dircount"]) = bestSize(filepath)
			else: 
				self["type"] = 'F'
				self["size"] = bestSize(filepath)
			self["mtime"] = getmtime(filepath)
			self["ctime"] = getctime(filepath)
		else: print filepath
	def __str__(self):
		l = ["%s" %self[i] for i in self]
		return "\t".join(l)
		
	def __repr__(self):
		return "<class gFile {path}".format(self)
		
def getAllFiles(path, filter=None, folder=False):
	lf = [] # list of all files
	ld = []	# list of all subfolders
	for root, dirs, files in  os.walk(path):
		# to improve performance I save only file paths. 
		for i in files: lf.append(os.path.join(root, i))
		for i in dirs: ld.append(os.path.join(root, i))
	if folder: l = ld
	else: l = lf
	l = [i for i in l if filter.match(i)]
	l = [gFile(i) for i in l]	
	return l
def parseFilter(filter, regex=False, casesensitive=False):
	if os.path.exists(filter): return filter
	filter = "^%s$" %filter
	if not(regex):
		filter = filter.replace(".", "\.")
		filter = filter.replace("*", ".*?")
	if not(casesensitive): filter = re.compile(filter, re.IGNORECASE)
	else: filter = re.compile(filter)
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Best list files command.")
	parser.add_argument('filter', 
	help="A pattern to filter results. Uses * and ? as in Windows standard dir command.")
	parser.add_argument("-d", "--dir", action="store_true", dest="showdir",
	help="Show only subfolders.")
	parser.add_argument("-a", "--all", action="store_true", dest="showall",
	help="Show both files and folders.")
	# To avoid that if invoked without parameters it returns an error
	parser.add_argument("-r", "--recurse", action="store_true", dest="recurse",
	help="Recurse in subfolders. It could be very slow.")
	
	parser.add_argument("-x", "--regex", action="store_true", dest="regex",
	help="Uses the pattern as a regular expression. Note: it is a perfect match on whole filename ^ $ are implicit..")
	parser.add_argument("-c", "--casesensitive", action="store_true", dest="casesensitive",
	help="By default, regex and normal pattern matching is case insensitive, with this option it become case sensitive...")
	
	if len(sys.argv)==1: args = parser.parse_args("*")
	else: args = parser.parse_args()
	print "{0} {1}".format('temp', bestsize('temp'))
	print "{0} {1}".format('test', bestsize('test'))
	print "{0} {1}".format('mona', bestsize('mona'))
	print "{0} {1}".format('persona-new.txt', bestsize('persona-new.txt'))
	print "{0} {1}".format('prova', bestsize('prova'))
	print "{0} {1}".format('d:\\musica', bestsize('d:\\musica'))
	