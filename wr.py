# Retrieves words translation from WordReference

# PyQuery is a very powerful module to parse HTML pages, but it is not by default distributed with Python
# if you want install it you need first install lxml module

import simplejson
import os
import sys

try:
	from pyquery import PyQuery as pq
	pqisloaded = True
except ImportError:
	pqisloaded = False
isredirected = False
pq.isredirected = isredirected

# Create an istance of FancyURLopener to avoid to be banned from certains sites that reject no browser user agent

from urllib import FancyURLopener, quote, quote_plus
class MyOpener(FancyURLopener):	
	version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.9.2.4) Gecko/20100513 Firefox/3.6.4"
	


def copyToClipboard(s):
	import pyperclip
	pyperclip.winSetClipboard(s)
		
def saveJSON(filename, data):
	f = open(filename, "w")
	simplejson.dump(data, f)
	f.close()
	
	
	
	

def openJSON(filename):
	f = open(filename, "r")
	if not(os.path.exists(filename)): return None
	f = open(filename, "r")
	data = simplejson.load(f)
	f.close()
	return data
	


def saveConfig(data):
	cfgpath = os.path.dirname(sys.argv[0])
	filename = os.path.join(cfgpath, "wrsettings.cfg")
	saveJSON(filename, data)
	
def loadConfig():
	cfgpath = os.path.dirname(sys.argv[0])
	filename = os.path.join(cfgpath, "wrsettings.cfg")
	if not(os.path.exists(filename)): 
		data = {"from" : "en", "to" : "it", "encodingenit" : "utf-8", "encodingiten" : "iso-8859-1"}
		saveJSON(filename, data)
	else: data = openJSON(filename)
	return data
	

def openURL(url):
	global isredirected
	""" Open a URL using the Firefox user agent to avoid to be banned from getting the page content """
	myopener = MyOpener()
	u = myopener.open(url)
	s = u.read()
	doc = pq(s)
	if url != u.url: doc.isredirected = True
	u.close()
	return doc
	

def formatter(s):
	s = s.replace(u"\u21d2", u"=>")
	return s
def getFromWRurl(url):
	d = openURL(url)
	encoding = d.encoding
	chunks = d("table.WRD")
	if len(chunks)==0: return None
	entries = []
	for i in range(len(chunks)):
		items = chunks.eq(i)("tr")
		for j in range(1, len(items)):
			entries.append(formatter(items.eq(j).text()))
	return entries
	

def getFromWR(word, lang1, lang2, pageencoding):
	word = quote(word.replace("-", " ").encode(pageencoding))
	url = "http://www.wordreference.com/%s%s/%s" %(lang1, lang2, word)
	return getFromWRurl(url)
	
def getDBFile(word, lang1, lang2):
	if isinstance(word, unicode): word = word.encode(sys.getfilesystemencoding())
	dbpath = os.path.dirname(sys.argv[0])
	filename = os.path.join(dbpath, "db", "%s%s" %(lang1, lang2), "%s.db" %word[0])
	return filename
def getFromLocalDB(word, lang1, lang2):
	filename = getDBFile(word, lang1, lang2)
	if not(os.path.exists(filename)): return None
	data = openJSON(filename)
	if not(data.has_key(word)): return None
	l = []
	if data[word].has_key("custom"): l.extend(data[word]["custom"])
	if data[word].has_key("wr"): l.extend(data[word]["wr"])
	if l==[]: return None
	return l


	
def updateLocalDB(word, desc, entrytype, lang1, lang2):
	filename = getDBFile(word, lang1, lang2)
	if not(os.path.exists(filename)):
		if not(os.path.exists(os.path.dirname(filename))): os.makedirs(os.path.dirname(filename))
		if isinstance(desc, unicode): desc = [desc]
		saveJSON(filename, {word : {entrytype : desc}})
	else:
		data = openJSON(filename)
		if data.has_key(word):
			if entrytype=="wr": data[word]["wr"] = desc
			elif entrytype=="custom":
				if data[word].has_key("custom"): data[word]["custom"].append(desc)
				else: data[word]["custom"] = [desc]
		else:
			if isinstance(desc, unicode): desc=[desc]
			data[word] = {entrytype : desc}
		saveJSON(filename, data)
		
		
def printentry(entry, toclip):
	if entry: s = u"\n".join(entry)
	else: s="Not Found,  sorry, I apologize!"
	print s.encode(sys.stdout.encoding, "replace")
	if toclip: copyToClipboard(s.encode(sys.getfilesystemencoding()))

def cmdget(args):
	global config
	if args.reverse: (args.fromlang, args.tolang) = (args.tolang, args.fromlang)
	if not(args.encoding): args.encoding=config["encoding%s%s" %(args.fromlang, args.tolang)]
	args.word = args.word.decode(sys.getfilesystemencoding()).lower()
	if args.useLocalDB: translated = getFromLocalDB(args.word, args.fromlang, args.tolang)
	elif args.useWRDB: translated = getFromWR(args.word, args.fromlang, args.tolang, args.encoding)
	else:
		# smart get with auto update of local DB
		# Try to open local DB to see if an entry exists, if not try to get it from WordReference
		translated = getFromLocalDB(args.word, args.fromlang, args.tolang)
		if not(translated):
			translated = getFromWR(args.word, args.fromlang, args.tolang, args.encoding)
			translated = getFromWR(args.word, args.fromlang, args.tolang, args.encoding)
			if (translated and config["autocollect"]): updateLocalDB(args.word, translated, "wr", args.fromlang, args.tolang)
	
	printentry(translated, args.clipboard)
	
def cmdedit(args):
	global config
	if not(args.wordmeaning or args.updateFromWR): raise argparse.ArgumentTypeError("You must provide a definition or retrieving it from WordReference.")
	if args.reverse: (args.fromlang, args.tolang) = (args.tolang, args.fromlang)
	args.word = args.word.decode(sys.getfilesystemencoding()).lower()
	if args.wordmeaning:
		args.wordmeaning = args.wordmeaning.decode(sys.getfilesystemencoding())
		updateLocalDB(args.word, args.wordmeaning, "custom" , args.fromlang, args.tolang)
	elif args.updateFromWR:
		if args.word[-1]=="*":
			if args.word=="*": downloadAllDB(args.fromlang, args.tolang)
			else: downloadAllPage(args.word[:-1], args.fromlang, args.tolang, config["encoding%s%s" %(args.fromlang, args.tolang)])
		else:
			translated = getFromWR(args.word, args.fromlang, args.tolang, config["encoding%s%s" %(args.fromlang, args.tolang)])
			if translated: updateLocalDB(args.word, translated, "wr", args.fromlang, args.tolang)
		
def printconfig():
	config = loadConfig()
	s=""
	for i in config: s+= "%-20s\t=\t%s\n" %(i, config[i])
	print s
	
def cmdcfg(args):
	global config
	if args.custom: 
		config[args.custom[0]] = args.custom[1]
		saveConfig(config)
	if (args.fromlang or args.tolang or args.encoding):
		config["from"] = args.fromlang if args.fromlang else config["from"]
		config["to"] = args.tolang if args.tolang else config["to"]
		if args.encoding:
			if (args.fromlang and args.tolang): config["encoding%s%s" %(args.fromlang, args.tolang)] = args.encoding
			else:
				print "To set character encoding of pages it is required to supply the source and final language."
				sys.exit(-2)
		saveConfig(config)
		print "Configuration successfully updated.n\n"
		printconfig()
	else: printconfig()

	
	

def cmdremove(args):
	print args
	if args.reverse: (args.fromlang, args.tolang) = (args.tolang, args.fromlang)
	word = args.word.decode(sys.getfilesystemencoding())
	filename = getDBFile(word, args.fromlang, args.tolang)
	nothing = False
	if not(os.path.exists(filename)): nothing = True
	else:
		data = openJSON(filename)
	if not(data.has_key(word)): nothing = True
	else:
		if args.wholeentry: del(data[word])
		else: del(data[word]["custom"])
		saveJSON(filename, data)
	if nothing: print "Nothing to delete."
	else: print "Entry successfully deleted. Congratulation!"

	
	
	
def customField(s):
	prefs = s.split("=")
	try:
		(prefname, prefvalue) = (prefs[0], prefs[1])
		if prefvalue.lower() in ["true", "false"]: prefvalue = bool(prefvalue)
		return (prefname, prefvalue)
	except IndexError:
		raise argparse.ArgumentTypeError("You must provide both preference name and preference value.")

def getPageLinksFromUrl(url):
	baseurl = "http://www.wordreference.com"
	page=openURL(url)
	links = page("#link a")
	easylinks = []
	for i in range(len(links)): easylinks.append({"href" : "%s%s" %(baseurl, links.eq(i).attr("href")), "text" :  links.eq(i).text()})
	return easylinks
	
def getPageLinks(first, lang1, lang2,  pageencoding):
	global config
	first = quote(first.replace("-", " ").encode(pageencoding))
	url = "http://www.wordreference.com/%s%s/%s" %(lang1, lang2, first)
	return getPageLinksFromUrl(url)

def downloadAllPage(first, lang1, lang2, pageencoding):
	links = getPageLinks(first, lang1, lang2, pageencoding)
	for i in links:
		translated = getFromWRurl(i["href"])
		print "%s definition saved on local DB" %i["text"]
		updateLocalDB(i["text"], translated, "wr", lang1, lang2)

def downloadPageFromUrl(url, lang1, lang2):
	""" Returns the last entry in the page for iterate. """
	links = getPageLinksFromUrl(url)
	for i in links:
		translated = getFromWRurl(i["href"])
		print "%s definition saved on local DB" %i["text"]
		updateLocalDB(i["text"], translated, "wr", lang1, lang2)
	return links[-1]
	
def downloadAllDB(lang1, lang2):
	print "Please stop it using CTRL+C when it reaches the last word in database."
	choice = raw_input("Do you have understood? Do you are ready?")
	if not(choice.lower() in ["y", "yes", "s", "si"]): sys.exit(-3)
	
	start = "http://www.wordreference.com/%s%s/alga" %(lang1, lang2)
	while True:
		last = downloadPageFromUrl(start, lang1, lang2)["href"]
		start = last

		
		
	
	
	
if __name__ == '__main__':
	import argparse
	config = loadConfig()
	parser = argparse.ArgumentParser(description="Retrieve translation from WordReference glossary.")
	subparsers = parser.add_subparsers(help="Commands", dest="command")
	configparser = subparsers.add_parser("cfg",  help="Set default settings.")
	removeparser = subparsers.add_parser("rm",  help="Remove an entry from localDB.")
	editparser = subparsers.add_parser("edit",  help="Add customized entries in glossary.")
	getparser = subparsers.add_parser("get",  help="Get word definitions.")
	getparser.add_argument('word',
	help="Word to search.")
	getparser.add_argument("-f","--from", dest="fromlang", default = config["from"],
	help="Source language. By default it uses language set in wrsettings.cfg file.")
	getparser.add_argument("-t","--to", dest="tolang", default = config["to"],
	help="Final language. By default it uses language set in wrsettings.cfg file.")
	getparser.add_argument("-r", "--reverse", action="store_true", dest="reverse",
	help="Reverse 'from' and 'to' language..")
	getparser.add_argument("-l", "--local", action="store_true", dest="useLocalDB",
	help="Get the definition from the local DB skipping WordReference DB.")
	getparser.add_argument("-w", "--remote", action="store_true", dest="useWRDB",
	help="Get the definition from WordReference skipping local DB..")
	getparser.add_argument("-c", "--clipboard", action="store_true", dest="clipboard",
	help="Copy output in clipboard (For the moment it supports only Windows).")
	getparser.add_argument("-e","-encoding", dest="encoding", default = None	,
	help="Character encoding of pages on WordReference, it's better configure it in .")
	configparser.add_argument("-c","--custom", type=customField, dest="custom", default = None,
	help="Set a default preference pref=value.")
	
	configparser.add_argument("-f","--from", dest="fromlang", default = None,
	help="Set up the source language in wrsettings.cfg.")
	configparser.add_argument("-t","--to", dest="tolang", default=None,
	help="Set up the final language in wrsettings.cfg.")
	configparser.add_argument("-e","-encoding", dest="encoding", default = None,
	help="Set up the page encoding.")
	editparser.add_argument('word',
	help="Word to edit.")
	editparser.add_argument("-d","--def", dest="wordmeaning", default = None,
	help="Meaning of the word, another entry in glossary.")
	editparser.add_argument("-r", "--reverse", action="store_true", dest="reverse",
	help="Reverse 'from' and 'to' language..")
	editparser.add_argument("-f","--from", dest="fromlang", default = config["from"],
	help="Source language.")
	editparser.add_argument("-t","--to", dest="tolang", default=config["to"],
	help="Final language.")
	editparser.add_argument("-w", "--wordreference", action="store_true", dest="updateFromWR",
	help="Update the local DB with the entry retrieved from WordReference).  Use word* to get all entries in a page. Use * to get whole DB (very slow).")
	
	removeparser.add_argument('word',
	help="Word to remove from localDB, by default only custom field.")
	removeparser.add_argument("-r", "--reverse", action="store_true", dest="reverse",
	help="Reverse 'from' and 'to' language..")
	removeparser.add_argument("-a", "--all", action="store_true", dest="wholeentry",
	help="Remove whole entry from localDB, by default it removes only custom field of an entry.")
	removeparser.add_argument("-f","--from", dest="fromlang", default = config["from"],
	help="Source language.")
	removeparser.add_argument("-t","--to", dest="tolang", default=config["to"],
	help="Final language.")
	if len(sys.argv)==1: 
		parser.print_help()
		sys.exit(2)

	args = parser.parse_args()
	if args.command=="cfg": cmdcfg(args)
	elif args.command=="get": cmdget(args)
	elif args.command=="edit": cmdedit(args)
	elif args.command=="rm": cmdremove(args)