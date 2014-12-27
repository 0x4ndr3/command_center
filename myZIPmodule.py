from zipfile import ZipFile
from threading import Thread

FOUND = None
def extractFile(zFile, password):
	global FOUND
	try:
		zFile.extractall(pwd=password)
		print '[+] Password = ' + password + '\n'
		FOUND = True
	except:
		pass

def bruteZip(zname, dname):
	global FOUND
	FOUND = False
	try:
		zFile = ZipFile(zname)
	except:
		print '[-] The provided file is not a ZIP file\n'
		return
	try:
		dictFile = open(dname,'r')
	except:
		print '[-] Could not open dictionary file "' + dic + '" (either it does not exist or you do not have permissions to read it\n'
		return
	threads = []
	for line in dictFile.readlines():
		word = line.strip('\n\r')
		t = Thread(target=extractFile, args=(zFile,word))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()
	if not FOUND:
		print '[-] Password not in the provided dictionary\n'