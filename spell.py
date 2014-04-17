# -*- coding: utf-8 

# Spell checker for .po and .lang files
# It uses Pyenchant: http://pythonhosted.org/pyenchant/tutorial.html
# and OpenOffice/LibreOffice dictionaries


try:
	import enchant # for spell check, install it first
except ImportError:
	print "Install pyenchant first to use this script..."
	webbrowser.open("http://pythonhosted.org/pyenchant/tutorial.html")
import re
import lang
import polib
from storage import storageData # To manage cache

def readListFiles(filename):
	import os
	f = open(filename, "r")
	l = f.read().split("\n")
	f.close()
	l = [i.strip() for i in l if os.path.exists(i.strip())]
	return l
	
	
def readFile(filename, **kwargs):
	import codecs
	encoding = kwargs.get("encoding", "utf-8")
	f = codecs.open(filename, "r", encoding, errors="replace")
	s = f.read()
	f.close()
	return s.split("\n")
	

def stripHTML(s):
	s = s.replace(u"’", u"'")
	mail_pattern = r"\w+@\w+\.\w+"
	url_pattern = r"http[s]*:\/\/[^\s,]+|\b\w+\.\w+\.\w+\b"
	html_pattern = r"<.*?>|&\w+;"
	var_pattern = r"%\(\w+\)s|%[dsS0-3$]"
	var2_pattern = r"\{[\w\.0-9-]+\}"
	s=re.compile("<br/*>").sub(' ', s)
	regex = re.compile("{0}|{1}|{2}|{3}|{4}".format(url_pattern, mail_pattern, html_pattern, var_pattern, var2_pattern))
	return regex.sub("", s)




def missSpelled(s, wordsfile="words.txt"):
	d = enchant.DictWithPWL("it_IT", wordsfile)
	words = re.compile(r"[\w'àèéìàù-]+", re.UNICODE).findall(stripHTML(s))
	err = []
	for i in words:
		if not(d.check(i)): err.append(i)
	if not(err): return False
	return err
def checkFile(filename, exclude=[]):
	filename = filename.strip()
	exclude = [i.strip() for i in exclude]
	cache = storageData("spell_cache.txt")
	if not(cache.get()):
		cache.clear()
		cache.save()
	(name, ext) = splitext(filename)
	ext = ext.lower()
	if ext==".po": inf = [i.msgstr for i in polib.pofile(filename)]
	elif ext==".lang": inf = [i.msgstr for i in lang.langFile(filename)]
	elif (ext==".txt") or (ext==".md"): inf = readFile(filename)
	else: raise IOError("Invalid file format.")
	errs = []
	cached = []
	if cache.isEmpty(): firstcache = {}
	else: firstcache = cache.get()
	if firstcache.has_key(filename): myrange = cache.get()[filename]
	else: myrange = range(len(inf))
	for i in myrange:
		if  inf[i].strip() in exclude: continue
		err = missSpelled(inf[i], wordsfile)
		if err:
			cached.append(i)
			print u"\n".join(err)
			errs.append("%s typo at line %s: %s ==> %s" %(len(err), i, "\t".join(err), inf[i]))
		firstcache[filename] = cached
		cache.update(firstcache)
		cache.save()
	return errs
	
	

if __name__ == '__main__':
	from os.path import dirname, splitext
	import argparse
	import sys
	parser = argparse.ArgumentParser(description="Make a spell check on a file. Supported formats: .lang, .po.")
	parser.add_argument('filename',
	help="File to spell check.")
	parser.add_argument("-f", "--from-file-list", action="store_true", dest="filelist",
	help="Spell check a list of files specified in a file. .")
	parser.add_argument("-e","--encoding", dest = "encoding", default = "utf-8",
	help="Charset encoding of the file,  by default it uses UTF-8..")
	wordsfile = "%s\\words.txt" %dirname(sys.argv[0])
	parser.add_argument("-x","--exclude", dest = "toexclude", default =  None,
	help="A file that contains a list of strings already verified and that will be excluded..")
	args = parser.parse_args()
	print args
	filename = args.filename
	if args.toexclude: 
		exclude = readFile(args.toexclude)
	else: exclude = []
	if args.filelist:
		filelist = readListFiles(args.filename)
	else:
		filelist = [args.filename]
	s = ""
	for i in filelist:
		errs = checkFile(i, exclude=exclude)
		if len(errs)>0: s+= "\nSpell check for %s\n\n" %i
		print "%s errrorsfound in %s" %(len(errs), i)
		s += "\n".join(errs)
		
	f = open("log.txt", "w")
	s = s.encode("utf-8", "replace")
	f.write(s)
	f.close()
	print "Log written in log.txt"