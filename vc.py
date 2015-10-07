import re
import subprocess
import sys
from urllib import urlencode


gdata = None # global variable
def numberize(x):
	if isinstance(x, int): return "%d" %x
	import re
	regex = re.compile(r"\d")
	test = regex.sub("", x)
	if test=="": return x
	else: return False
	return test
	
def joinurl(u1, u2):
	if u1[-1]=="/" and u2[0]=="/": return "{0}{1}".format(u1, u2[1:])
	elif u1[-1]!="/" and u2[0]!="/": return "{0}/{1}".format(u1, u2)
	else: return "{0}{1}".format(u1, u2)
	

class urlmodel():
	def __init__(self, url):
		self.url = url
	def __add__(self, s):
		self.url = joinurl(self.url, s)
		return self
		
	def __repr__(self):
		return self.url
		
	def query(self, args):
		self.url = "{0}?{1}".format(self.url, urlencode(args))
		
	def format(self, style="text", desc=""):
		model = {
		"markdown" : "[{1}]({0}",
		"html" : '<a href="{0}">{1}</a>',
		"bbcode" : "[url={0}]{1}[/url]"
		}
		if style=="text": return self.url
		if not(model.has_key(style)): raise ValueError("Style not supported. Available styles are: text (default), markdown, html and bbcode.")
		if desc=="": desc = self.url
		return model[style].format(self.url, desc)


def getsvninfo():
	global gdata
	""" Get path and revision number using svn info"""
	revregex = re.compile(r'^Revision:\s*([0-9]+)$', re.MULTILINE)
	urlregex = re.compile(r'^URL:\s*(.*)$', re.MULTILINE)
	urlregex2 = re.compile(r'^Repository Root:\s*(.*)$', re.MULTILINE)
	try:
		output = subprocess.check_output(["svn", "info"], stderr=subprocess.STDOUT)
		revnumber = revregex.search(output).group(1)
		url = urlregex.search(output).group(1)
		url2 = urlregex2.search(output).group(1)
		data = {"url" : url, "root" : url2, "rev" : revnumber, "relative" : url.replace(url2, "")}
		if gdata: gdata.update(data)
		else: gdata = data
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
		data = {"M" : modified, "A": added, "U" : unknown}
		if gdata: gdata.update(data)
		else: gdata = data
	except subprocess.CalledProcessError:
		print "Unable to check status, sorry"
		sys.exit(-1)
		
def makesvncommit(message):
	global gdata
	""" Make a commit of modified files to svn server. Use with care."""
	regex = re.compile(r"^Sending\s*(.*)$", re.MULTILINE)
	regex2 = re.compile(r"^\s*Committed revision (\d+)\.", re.MULTILINE)
	try:
		output = subprocess.check_output(["svn", 'commit -m "{0}"'.format(message)], stderr=subprocess.STDOUT)
		print output # only for debug, remove it
		committed = regex.findall(output)
		revnumber = regex2.match(output).group(1)
		data = {"committed" : committed, "rev" : revnumber}
		if gdata: gdata.update(data)
		else: gdata = data
	except subprocess.CalledProcessError:
		print "Something goes wrong making the commit, sorry. Try again later."
		sys.exit(-1)

def getcommiturl(revnumber=None):
	url = urlmodel("http://viewvc.svn.mozilla.org/vc/")
	global gdata
	if not(revnumber): 
		if not(gdata): getsvninfo()
		if not(gdata.has_key("rev")): getsvninfo()
		revnumber = gdata["rev"]
	else:
		revnumber = numberize(revnumber)
	url.query([("view", "revision"), ("rev", revnumber)])
	return url
		
def getfileurl(filepath, vctype=True, revnumber=None, vcview="co"):
	global gdata
	filepath = filepath.replace("\\", "/")
	if not(gdata): getsvninfo()
	if not(gdata.has_key("url")): gdata.getsvninfo()
	if not(vctype):
		url = urlmodel(gdata["url"])
		url = url + filepath
	else:
		url = urlmodel("http://viewvc.svn.mozilla.org/vc/")
		url += (gdata["relative"] ) + filepath
		query = []
		if revnumber: query.append(("rev", revnumber))
		query.append(("view", "co"))
		url.query(query)
	return url
	
def printOutput(s, clipboard=True):
	import pyperclip
	print s
	if clipboard: pyperclip.winSetClipboard(s)
	
def cmdview(filepath, vctype = True, rev=None, clipboard=True):
	from os import path
	if filepath=="rev": printOutput(getcommiturl())
	if not(path.exists(filepath)): raise ValueError("File not exists.")
	s = getfileurl(filepath, vctype)
	printOutput(s, clipboard)
	
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Help to find the remote link of a SVN file.")
	subparsers = parser.add_subparsers(help="Commands", dest="command")
	viewparser = subparsers.add_parser("view",  help="Show online version.")
	revparser = subparsers.add_parser("rev",  help="Show the commit page..")
	diffparser = subparsers.add_parser("diff",  help="Show the online diff")
	viewparser.add_argument("filepath", 
	help = "The file in your local folder. It returns its remote path.")
	viewparser.add_argument("-s", "--svn", action = "store_true", default=False,
	help = "Show the URL on svn server not vcview.")
	viewparser.add_argument("-c", "--clipboard", default=True, action="store_false",
	help = "If specified the output is copied in your clipboard for easy pasting.")
	viewparser.add_argument("-r", "--rev", 
	help = "The revision number of the file. It uses vc view by default.")
	args = parser.parse_args()
	print args.command
	print args
	if args.command=="view": cmdview(args.filepath, not(args.svn), args.rev, args.clipboard)
	elif args.command=="rev": cmdrev(args.revnumber, args.clipboard)