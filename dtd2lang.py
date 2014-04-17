from translate.storage import dtd
import lang
from collections import OrderedDict

def openDTD(file):
	f = open(file, "r")
	dtdobj = dtd.dtdfile(f)
	f.close()
	dtdentries = dtdobj.units
	d = OrderedDict()
	for i in dtdentries:
		if d.has_key(i.entity): print "Duplicate entry: %s" %i.entity
		else: d[i.entity] = dtd.unquotefromdtd(i.definition)
	return d
	
		
def createlangfile(file):
	from os import path
	filename = path.split(file)[1]
	filenamewext = path.splitext(filename)[0]
	src = openDTD("..\\en-US\\%s" %filename)
	dst = openDTD(file)
	lf = lang.langFile("%s.lang" %filenamewext)
	for i in src:
		if dst.has_key(i): lf.append(src[i], dst[i])
		else:
			print "Missing translation: %s" %i
			lf.append(src[i], src[i])
	lf.save()
	
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Export DTD files in lang format.")
	parser.add_argument('inputfilename',
	help="Input filename in dtd format.")
	args = parser.parse_args()
	print args.inputfilename
	dtdentries = openDTD(args.inputfilename)
	print len(dtdentries)
	createlangfile(args.inputfilename)