# Simple storage script to use simplejson or fallback to pickle standar module if simplejsoN is not available

import pickle
try:
	import simplejson
	sjavailable = True
	defaultStorageAPI = "simplejson"
except ImportError:
	sjavailable = False
	defaultStorageAPI = "pickle"


class storageData(object):
	def __init__(self, filename, **kwargs):
		_openfile = kwargs.get("open", True)
		storageAPI = kwargs.get("storageAPI", defaultStorageAPI)
		self.filename = filename
		if storageAPI == "simplejson":
			if sjavailable: self.__storageAPI = simplejson
			else: raise ImportError("simplejson is not available. Please install it, in short 'pip install simplejson'")
		elif storageAPI =="pickle": 
			self.__storageAPI = pickle
		else: raise TypeError("You can use only simplejson or pickle")
		if _openfile:
			try:
				self.open()
			except IOError:
				self._data = kwargs.get("defaultData", None)
		else: self._data = kwargs.get("defaultData", None)

	def open(self):
		from os.path import exists
		if not(exists(self.filename)): raise IOError("Data file not exists.")
		f = open(self.filename, "r")
		self._data = self.__storageAPI.load(f)
		f.close()

	def update(self, data):
		self._data = data
		
	def save(self):
		f = open(self.filename, "w")
		self.__storageAPI.dump(self._data, f)
		f.close()
		
		
	def get(self):
		return self._data
	def clear(self):
		self.update("__EMPTY__")
		self.save()
		
		
	def isEmpty(self):
		return self._data=="__EMPTY__"
def pickle2json(filename):
	if not(sjavailable): raise ImportError("You must install simplejson to convert data file to json format. In short, 'pip install simplejson'")
	a = storageData(filename, storageAPI = "pickle")
	a = storageData(filename, storageAPI = "simplejson", open=False)
	b.update(a.get())
	b.save()
def json2pickle(filename):
	if not(sjavailable): raise ImportError("You must install simplejson to convert data file from json format. In short, 'pip install simplejson'")
	a = storageData(filename, storageAPI = "simplejson")
	b = storageData(filename, storageAPI = "pickle", open=False)
	b.update(a.get())
	b.save()
	
	
if __name__=='__main__':
	print "ciao"