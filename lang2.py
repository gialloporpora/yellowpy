from sys import stdout
import polib

class msgmarker(polib.POEntry):
	def __init__(self, **kwargs):
		polib.POEntry.__init__(self, **kwargs)
		if self.comment=='': self.comment=[]
		else: self.comment = [self.comment]
		if self.tcomment: self.comment.append(self.tcomment)
		
	def __unicode__(self):
		ret = ""
		if self.occurrences:
			filelist = []
			for fpath, lineno in self.occurrences:
				if lineno:
					filelist.append('%s:%s' % (fpath, lineno))
				else:
					filelist.append(fpath)
			filestr = ' '.join(filelist)
			ret += "#: {0}".format(filestr)
		if self.comment: ret += "\n[0}".format(u"\n#".join(self.comment))
			
		return ret