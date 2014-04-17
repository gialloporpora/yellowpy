from time import strftime, localtime, gmtime



def setSystemTime(dt):
	from win32api import SetSystemTime
	SetSystemTime(dt[0], dt[1], dt[6], dt[2], dt[3], dt[4], dt[5]+1, 0)

def getFromNTP(ntpserver="time.windows.com"):
	import ntplib
	c = ntplib.NTPClient()
	# The exception raised if server not responds is ntplib.NTPException
	response = c.request(ntpserver)
	return response.tx_time
	
	
def copyToClipboard(s):
	import pyperclip
	pyperclip.winSetClipboard(s)
	
def getcmd(args):
	if args.remote: mytime = localtime(getFromNTP())
	else: mytime = localtime()
	date = strftime("%d/%m", mytime)
	time = strftime("%H:%M", mytime)
	if args.showdate:s = "%s %s" %(date,time)
	else: s = time
	copyToClipboard(s)
	

	
def setcmd(args):
	print args.datetime
	dt = args.datetime
	if dt in ["auto", "sync", "ntp"]: dt = gmtime(getFromNTP())
	setSystemTime(dt)
		
if __name__ == '__main__':
	from sys import argv
	import argparse
	
	parser = argparse.ArgumentParser(description="cOPY TIME, AND OPTIONALLY DATE, TO CLIPBOARD")
	subparsers = parser.add_subparsers(help="Commands", dest="command")
	getparser = subparsers.add_parser("get",  help="Get date and time.")
	setparser = subparsers.add_parser("set",  help="Set date and time. Use sync or auto to use the NTP server to get the time.")
	getparser.add_argument("-d", "--date", action="store_true", dest="showdate",
	help="Show date too.")
	getparser.add_argument("-r", "--remote", action="store_true", dest="remote",
	help="Get time info from remote NTP server.")
	setparser.add_argument('datetime',
	help="Datetime to change. Use auto, sync, ntp to use the NTP server.")
	args = parser.parse_args()
	if args.command == "set": setcmd(args)
	elif args.command=="get": getcmd(args)
	
	