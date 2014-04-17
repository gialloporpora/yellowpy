import re
import subprocess
import sys
import urllib



class urlmodel():
	def __init__(self, root):
		self.root = root
		self.url = root
	def build(self, relpath="", query=None):
		url = urllib.basejoin(self.root, relpath)
		if query:
			querystring = urllib.urlencode(query)
			url+= "?%s" %querystring
		self.url = url
	def __repr__(self):
		return self.url
		
	def format(self, style=None, desc=""):
		model = {
		"markdown" : "[{1}]({0}",
		"html" : '<a href="{0}">{1}</a>',
		"bbcode" : "[url={0}]{1}[/url]"
		}
		if not(style): return self.url
		if not(model.has_key(style)): raise ValueError("Style not supported. Available styles are: markdown, html and bbcode.")
		if desc=="": desc = self.url
		return model[style].format(self.url, desc)


def getsvninfo():
	""" Get path and revision number using svn info"""
	revregex = re.compile(r'^Revision:\s*([0-9]+)$', re.MULTILINE)
	urlregex = re.compile(r'^URL:\s*(.*)$', re.MULTILINE)
	urlregex2 = re.compile(r'^Repository Root:\s*(.*)$', re.MULTILINE)
	try:
		output = subprocess.check_output(["svn", "info"], stderr=subprocess.STDOUT)
		revnumber = revregex.search(output).group(1)
		url = urlregex.search(output).group(1)
		url2 = urlregex2.search(output).group(1)
		return {"url" : url, "root" : url2, "rev" : revnumber, "relative" : url.replace(url2, "")}
	except subprocess.CalledProcessError:
		print "Sorry, this is not a SVN folder"
		sys.exit(-1)


def getsvnstatus():
	""" Get information about files to be committed """
	regex = re.compile(r"^M\s*(.*)$", re.MULTILINE)
	regex2 = re.compile(r"^\?\s*(.*)$", re.MULTILINE)
	regex3 = re.compile(r"^A\s*(.*)$", re.MULTILINE)
	try:
		output = subprocess.check_output(["svn", "status"], stderr=subprocess.STDOUT)
		modified = regex.findall(output)
		unknown = regex2.findall(output)
		added = regex3.findall(output)
		return {"M" : modified, "A": added, "U" : unknown}
	except subprocess.CalledProcessError:
		print "Unable to check status, sorry"
		sys.exit(-1)
		
def makesvncommit(message):
	""" Make a commit of modified files to svn server. Use with care."""
	regex = re.compile(r"^Sending\s*(.*)$", re.MULTILINE)
	regex2 = re.compile(r"^\s*Committed revision (\d+)\.", re.MULTILINE)
	try:
		output = subprocess.check_output(["svn", 'commit -m "{0}"'.format(message)], stderr=subprocess.STDOUT)
		print output # only for debug, remove it
		committed = regex.findall(output)
		revnumber = regex2.match(output).group(1)
		return {"committed" : committed, "rev" : revnumber}
	except subprocess.CalledProcessError:
		print "Something goes wrong making the commit, sorry. Try again later."
		sys.exit(-1)
		
def getfileurl(filepath, vctype="vc", revnumber=None, vcview="co"):
	filepath = filepath.replace("/", "\\")
	data = getsvninfo()
	if vctype=="svn":
		url = urlmodel(data["root"])
		url.build(filepath)
	elif vctype=="vc":
		url = urlmodel("http://viewvc.svn.mozilla.org/vc")
		query = []
		if revnumber: query.append(("rev", revnumber))
		query.append(("view", "co"))
	else: raise ValueError("vctype argument could be svn or vc.")
	return url

		
def cmdview(filepath, vctype=True, rev=None, clipboard=True):
	pass
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Help to find the remote link of a SVN file.")
	subparsers = parser.add_subparsers(help="Commands", dest="command")
	viewparser = subparsers.add_parser("view",  help="Show online version.")
	diffparser = subparsers.add_parser("diff",  help="Show the online diff")
	args = parser.parse_args()
	print args.command