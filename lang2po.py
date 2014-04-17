import polib
import lang


if __name__ == '__main__':
	import sys
	from os.path import splitext
	filename = sys.argv[1]
	(name, ext) = splitext(filename)
	po = polib.POFile()
	po.encoding = "UTF-8"
	po.metadata["Project-Id-Version"] = u"%s 1.0" %name
	po.metadata["Language"] = u"it"
	po.metadata["Content-Transfer-Encoding"] = "8bit"
	po.metadata["Content-Type"] = u"text/plain; charset=UTF-8"
	po.metadata["Plural-Forms"] = u"nplurals=2; plural=(n != 1);"
	po.metadata["Language-Team"] = u"mozillaitalia"
	lf = lang.langFile(filename)
	for i in range(len(lf)):
		msgentry = polib.POEntry(msgid=lf[i].msgid, msgstr=lf[i].msgstr, occurrences=[("%s.py" %name, i)])
		po.append(msgentry)
	po.save("%s.po" %name)
	