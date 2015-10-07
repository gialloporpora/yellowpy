import re
from lang import *
import polib
import argparse
from os.path import splitext, exists

def ignoreIdentical(s):
	regex = re.compile(r"\s*\{ok\}\s*$", re.IGNORECASE)
	return regex.sub("", s)
	

	
def wordsCounter(s, ignoreShorterThan=3):
	s = s.lower()
	# Removing HTML code
	rh = re.compile(r"<.*?>")
	s = rh.sub("", s)
	regex = re.compile(r"\b\w+\b")
	items = regex.findall(s)
	d = {}
	for i in items:
		if len(i)> ignoreShorterThan:
			if i in d: d[i] = d[i]+1
			else: d[i] = 1
			l = []
			for i in d:
				l.append({"word" :i, "count" : d[i]})
	l.sort(lambda x, y: cmp(y["count"], x["count"]))
	return l
	
def isFuzzy(self):
	return "fuzzy" in self.flags

def hasPlural(self):
	return self.msgid_plural!=""
	
def normalizePO(po):
	""" normalize a po object putting into an a list plural directly on msgstr and msgid properties """
	for i in range(len(po)):
		if po[i].hasPlural():
			po[i].msgid= [po[i].msgid]
			if not(isinstance(po[i].msgid_plural, list)): po[i].msgid_plural = [po[i].msgid_plural]
			po[i].msgid.extend(po[i].msgid_plural)
			po.msgstr = po[i].msgstr_plural
	return po
			
	return po
def markFuzzy(self):
	self.flags.append(u'fuzzy')
	
polib.POEntry.isFuzzy  = isFuzzy  # Monkey Patching 
polib.POEntry.hasPlural  = hasPlural  # Monkey Patching 
polib.POEntry.markFuzzy  = markFuzzy  # Monkey Patching 
def fileType(filename):
	ext = splitext(filename)[1].lower()
	if ext==".pot": ext = ".po"
	return ext
def levenshtein_distance(first, second):
	"""Find the Levenshtein distance between two strings."""
	if len(first) > len(second):
		first, second = second, first
	if len(second) == 0:
		return len(first)
	first_length = len(first) + 1
	second_length = len(second) + 1
	distance_matrix = [[0] * second_length for x in range(first_length)]
	for i in range(first_length):
		distance_matrix[i][0] = i
	for j in range(second_length):
		distance_matrix[0][j]=j
	for i in xrange(1, first_length):
		for j in range(1, second_length):
			deletion = distance_matrix[i-1][j] + 1
			insertion = distance_matrix[i][j-1] + 1
			substitution = distance_matrix[i-1][j-1]
			if first[i-1] != second[j-1]:
				substitution += 1
			distance_matrix[i][j] = min(insertion, deletion, substitution)
	return distance_matrix[first_length-1][second_length-1]

def percentDiff(a, b):
	if a==b: return 0
	if a.lower()==b.lower(): return 0.1
	return 100*levenshtein_distance(a, b) / float(max(len(a), len(b)))		
	
	
def cmdStats(args):
	ext1 = fileType(args.filename)
	if ext1 in [".po", ".pot"]: file = polib.pofile(args.filename)
	elif ext1==".lang": file = langFile(args.filename)
	else: raise TypeError("Invalid input file, sorry!")
	s = ""
	for i in file:
		s += "%s " %i.msgid
	stats = wordsCounter(s)
	s = ""
	for i in stats:
		s += "%(word)s -> %(count)s\n" %i
	f = open("stats-%s.txt" %args.filename, "w")
	f.write(s)
	f.close()
	# Printing the first 10 results
	for i in range(10):
		print "%(word)s -> %(count)s" %stats[i]
	print "\n...\n.. for whole words occurences open stats-%s.txt\n" %args.filename
	

def cmdexport(args):
	""" export strings from a po, .pot or .lang file into a lang file. """
	if args.output=='default': outputfile = "%s.lang" %splitext(args.filename)[0]
	else: outputfile = args.output
	if args.untranslated: outputfile = "untranslated-%s" %outputfile
	newlang = langFile(outputfile)
	ext1 = splitext(args.filename)[1]
	if ext1==".lang": f = langFile(args.filename)
	else: f = polib.pofile(args.filename)
	if args.untranslated: f = f.untranslated_entries()
	if args.fuzzy: f = f.fuzzy_entries()
	for i in f:
		if i.translated() or  i.isFuzzy():
			if i.msgid==i.msgstr: i.msgstr = "%s {ok}" %i.msgstr
			newlang.append(i.msgid, i.msgstr)
		else: newlang.append(i.msgid, i.msgid)
	newlang.save()
	
		
	
	
def cmdcompile		(args):
	if fileType(args.filename)!=".po": raise argparse.ArgumentTypeError("This operation could be performed only with .po files")
	po = polib.pofile(args.filename)
	if args.output=='default': outputfile = "%s.mo" %splitext(args.filename)[0]
	else: outputfile = args.output
	po.save_as_mofile(outputfile)
	
def cmdinfo(args):
	if fileType(args.filename)==".po":
		f = polib.pofile(args.filename)
	elif fileType(args.filename)==".lang":
		f = langFile(args.filename)
	else: raise TypeError("unsupported file format")
	wc = re.compile(r"\b\w+\b")
	s = ""
	for i in f:
		s += "%s " %i.msgid
	totwords = len(wc.findall(s))
	s = ""
	uw= f.untranslated_entries()
	for i in uw:
		s+="%s " %i.msgid
	untwords = len(wc.findall(s))
	print "\nTotal strings: %s\nUntranslated strings: %s\nFuzzy strings: %s\nTotal words: %s\nUntranslated words: %s\n\n" %(len(f), len(f.untranslated_entries()), len(f.fuzzy_entries()), totwords, untwords)
	if args.untranslated:
		s = ''
		for i in f.untranslated_entries(): s+="%s\n\n" %i.msgid
		print s.encode("cp850", "replace")
	

def cmdmerge(args):
	ext1=fileType(args.filename)
	ext2 = fileType(args.filename2)
	if not(ext1 in [".pot", ".po", ".lang"]): raise TypeError ("Invalid input file type.")
	if not(ext2 in [".po", ".lang", ".txt"]): raise TypeError ("Invalid source for merging files")
	if (ext1 in ["po", ".pot"]) and (ext2==".po"): po = polib.pofile(args.filename).merge(args.filename2)
	elif ext2==".lang":
		fromlang = langFile(args.filename2)
		d = fromlang.getAsDict()
		if ext1 in [".po", ".pot"]:
			po = polib.pofile(args.filename)
			for i in po:
				if (d.has_key(i.msgid)) and (i.msgid!= d[i.msgid]):
					i.msgstr = ignoreIdentical(d[i.msgid])
			po.save()
		elif ext1==".lang":
			f = langFile(args.filename)
			f.updateFromDict(d, args.untranslated)
			f.save()
	elif (ext2==".txt") and (ext1==".lang"): a.updateFromOrderedTXT(args.filename2)
	
	else: raise TypeError ("something goes wrong. This operation is not available for these files, sorry!")
		
		


		

def exportToHTML(args):
	ext1 = fileType(args.filename)
	if ext1 in [".po", ".pot"]: file = polib.pofile(args.filename)
	elif ext1==".lang": file = langFile(args.filename)
	css ='body{background: #000;font-family: Arial, sans-serif;color: #fff}\n.original{color: yellow}.translated{font-weight: 900;color: #fff;}'
	s = '<!DOCTYPE HTML>\n<html>\n<head>\n<title>\n%s\n</title>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n<style type="text/css">\n%s\n</style>\n</head>\n<body>' %(args.filename, css)
	s+='\n<ul>\n'
	for i in file: s+='<li><span class="original">%(msgid)s</span> <span class="translated">%(msgstr)</span></li>\n' %i
	s+="</ul>\n</body>\n</html>"
	print s
	
if __name__ == '__main__':
	from shutil import copyfile
	parser = argparse.ArgumentParser(description="Tool to works with .po and .lang files.")
	# group = parser.add_mutually_exclusive_group()
	parser.add_argument('filename',
	help="Input filename, a po, pot or lang file")
	parser.add_argument("-m","--merge", dest="filename2", default = None,
	help="File to merge, it could be a .po, .pot, .lang or .txt (ordered) file")
	parser.add_argument("-e", "--export", action="store_true",
	help="Available only for po or po files, Export strings  as .lang file.")
	parser.add_argument("-s", "--stats", action="store_true",
	help="Shows word counting (very slow)..")
	parser.add_argument("-c", "--compile", action="store_true",
	help="Available only for po or po files, generate the .mo file.")
	parser.add_argument("-i", "--info", action="store_true",
	help="Show info about file.")
	parser.add_argument("-b", "--backup", action="store_true",
	help="Create a backup (.bak) copy of the input file.")
	parser.add_argument("-f", "--fuzzy", action="store_true",
	help = "Show fuzzy strings.")
	parser.add_argument("-u", "--untranslated", action="store_true",
	help = "Show untranslated strings.")
	parser.add_argument("-o","--output", default="default",
	help="Specify an output filename, if not specified the script assign a default filename inherited by input filename.")
	

	
	args = parser.parse_args()
	if args.backup: copyfile(args.filename, "%s.bak" %args.filename)
	if args.stats: cmdStats(args)
	if args.export: cmdexport(args)
	if args.filename2: cmdmerge(args)
	if args.compile: cmdcompile(args)
	if args.info: cmdinfo(args)