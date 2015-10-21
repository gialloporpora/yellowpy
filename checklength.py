# -*- coding: utf-8 -*-

import lang
import os.path

def getLimit(n1, limit):
	import re
	regex = re.compile(r"(\+)*\s*(\d+)\s*(%)*")
	m = regex.match(limit.strip())
	if m:
		val = m.group(2)
		if not(m.group(1)) and not(m.group(3)): totlen = int(m.group(2))
		elif m.group(1): totlen = n1 + int(m.group(2))
		elif m.group(3): totlen = int(n1 *( int(m.group(2)) + 100) / 100)
		else: raise ValueError("Value not accepted.")
		return totlen
		
		
	
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Check string length in .lan files.")
	parser.add_argument("inputfile",
	help=".lang file to check.")
	
	parser.add_argument("-l","--limit", dest="limit", default = "50%",
	help="Limit of translated string. You can use percentages (50%), fixed length (140) or a relative measure (+30) to specify the number of extra characters in translated string ")
	args = parser.parse_args()
	inf = lang.langFile(args.inputfile)
	outf = open("stats-%s" %args.inputfile, "w")
	s = u""
	for i in inf:
		nc1 = len(i.msgid)
		nc2 = len(i.msgstr)
		s+= u"# Originale: %d caratteri, traduzione: %d caratteri, differenza: %+d caratteri\n" %(nc1, nc2, nc2-nc1)
		if nc2 < nc1: s+= u"# Avviso: la traduzione è più corta dell'originale\n"
		if nc2 > getLimit(nc1, args.limit): s+= u"# Errore: limite superato\n"
		s+= u";%s\n%s\n\n\n" %(i.msgid, i.msgstr)
	outf.write(s.encode("utf-8"))
	outf.close()
	