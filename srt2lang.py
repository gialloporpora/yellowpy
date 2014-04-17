from os.path import splitext



def getTimeRegex(multiline=False):
	import re
	rt = r'\d\d:\d\d:\d\d(?:,\d\d\d)*'
	if multiline:
		rts = r'\d+' + '\n' + '%s\s*-->\s*%s' %(rt, rt)
		regex = re.compile(rts, re.MULTILINE)
	else:
		rts = r'%s\s*-->\s*%s' %(rt, rt)
		regex = re.compile(rts)
	return regex
	
	
def isTime(s):
	regex = getTimeRegex()
	return regex.match(s)
	
def openFile(filename):
	f = open(filename, "r")
	stream = f.read().decode('iso8859')
	f.close()
	return rearrange(stream)


def rearrange(s):
	regex = getTimeRegex(True)
	l1 = [i.strip().replace("\n", "\\\\") for i in regex.split(s)]
	regex = getTimeRegex()
	l2 = [i.strip() for i in regex.findall(s)]
	l3 = []
	del l1[0]
	for i in range(len(l2)):
		l3.append({"index" : l2[i], "msgid" : l1[i]})
	return l3
	
	
def srt2lang(filename, encoding="utf-8"):
	l = openFile(filename)
	stream = ""
	f = open("%s.lang" %splitext(filename)[0], "w")
	for i in l:
		stream += u"# %s\n;%s\n%s\n\n\n" %(i["index"], i["msgid"], i["msgid"])
	f.write(stream.encode(encoding))
	f.close()

		
	
if __name__ == '__main__':
	import sys
	filename = sys.argv[1]
	print filename
	srt2lang(filename)
	print "Done."