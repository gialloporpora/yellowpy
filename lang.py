from sys import stdout

class msgmarker(object):
	def __init__(self, msgid, msgstr, index, encoding="utf-8"):
		self._encoding =encoding
		self.set(msgid, msgstr)
		self._index = index
		
	def __repr__(self):
		return "<msgmarker object>"
		
	def __str__(self):
		u = u'msgid: "%s"\nmsgstr: "%s"' %(self.msgid, self.msgstr)
		return u.encode(stdout.encoding, "replace")

	def isTranslated(self):
		return self._msgstr!=self.msgid
		
	def translated(self):
		""" Duplicated for convenience with polib.poentry class """
		return self.isTranslated()
		
	def isFuzzy(self):
		return self._msgstr[0:2]=="=="

	def markFuzzy(self):
		self._msgstr = "==%s" %(self.msgstr)
		

	def set(self, msgid, msgstr):
		if not(isinstance(msgid, unicode)): msgid = msgid.decode(self._encoding)
		self.msgid = msgid
		self.setmsgstr(msgstr)
		
	def setmsgstr(self, msgstr):
		if not(isinstance(msgstr, unicode)): msgstr = msgstr.decode(self._encoding)
		self._msgstr = msgstr
		self.msgstr = self.getmsgstr()
		
	def getmsgid(self):
		return self.msgid
		

	def getrawmsgstr(self):
		return self._msgstr
		
	def getmsgstr(self):
		import re
		regex=re.compile("^==|\s{ok}$", re.IGNORECASE)
		return regex.sub("", self._msgstr)
		
	def getIndex(self):
		return self._index
	def getIndex(self):
		return self._index
	
		

class langFile(list):
	def __init__(self, name, encoding="utf-8"):
		self._name = name
		self._encoding = encoding
		self._index = 0 # This is used to implement iteration, it is not the index used to track the number line
		try:
			self._list = self.open()
			self._strings = self._getStrings()
			if len(self)==0: raise TypeError("This file is not a valid lang file")
			self._last = self._strings[-1].getIndex() + 1
		except IOError:
			self._list = []
			self._strings = []
			self._last = 0
		
	def __getitem__(self, index):
		return self._strings[index]
		
	def __setitem__(self, index, value):
		""" Modyfy only the msgstr part, msgid and index are private data """
		self._strings[index].setmsgstr(value)
		self._list[self._strings[index].getIndex()] = self._strings[index]._msgstr
	
	def __repr__(self):
		return "<langFile object: %s>" %self._name

	def __len__(self):
		return len(self._strings)
	def __iter__(self):
		return self
		
	def next(self):
		if self._index == len(self):
			self._index = 0
			raise StopIteration
		next = self._index
		self._index += 1
		return self._strings[next]
	def __str__(self):
		s = ""
		for i in self:
			s += ";%s\n%s\n\n\n" %(i.msgid, i.msgstr)
		return s.encode(stdout.encoding, 'replace')

	def append(self, msgid, msgstr):
		el = msgmarker(msgid, msgstr, self._last +4)
		self._strings.append(el)
		if (self._last>=len(self._list)) or (len(self)==1):
			if len(self) > 1:
				self._list.append("")
				self._list.append("")
			self._list.append(";%s" %el.msgid)
			self._list.append("%s" %el._msgstr)
		else:
			self._list.insert(self._last, "%s" %el._msgstr)
			self._list.insert(self._last, ";%s" %el.msgid)
			self._list.insert(self._last, "")
			self._list.insert(self._last,  "")
		self._last += 4



	def open(self):
		f = open(self._name, "r")
		l = f.read().decode(self._encoding, 'replace').split("\n")
		f.close()
		return l
	def _getStrings(self):
		k = []
		for i in range(len(self._list)):
			if self._list[i]!="":
				if self._list[i][0]==";":
					x = msgmarker(self._list[i][1:], self._list[i + 1], i+1)
					k.append(x)
		return k
		
	def getAsDict(self):
		d = {}
		for i in self:
			d[i.msgid] = i.msgstr
		return d
		
	def untranslated_entries(self):
		return [i for i in self if not(i.isTranslated())]
		
	def fuzzy_entries(self):
		return [i for i in self if i.isFuzzy()]
	
	
	def save(self):
		f = open(self._name, "w")
		f.write("\n".join(self._list).encode("utf-8"))
		f.close()
		
	def updateFromOrderedList(self, l):
		if len(l)!=len(self): raise TypeError( "Error: two file have different strings number")
		for  i in range(len(self)-1) :
			self[i] = l[i]

	def saveAsTXT(self):
		f = open("%s.txt" %self._name, "w")
		f.write("\n".join([i.msgstr for i in self]).encode("utf-8"))
		f.close()
		
	def updateFromDict(self, d, onlyUntranslated=True):
	# I need to access element by index since __setitem__ method update the self._list object
		for i in range(len(self)):
			if onlyUntranslated:
				if not(self[i].isTranslated()): 
					if d.has_key(self[i].msgid): self[i] =d[self[i].msgid]
			elif d.has_key(self[i].msgid): self[i] = d[self[i].msgid]
	
		
				

	def saveAsHTML(self):
		pass
		