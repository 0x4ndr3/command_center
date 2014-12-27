import pexpect

PROMPT =['# ', '>>> ', '> ', '\$ ']

class Zombie:
	def __init__(self, host, user, password, port=22, pwdAuth='yes'):
		self.host = host
		self.user = user
		self.password = password
		self.port = port
		self.pwdAuth = pwdAuth
		
	def __eq__(self, zombie):
		return self.host == zombie.host

	def connect(self):
		ssh_newkey = 'Are you sure you want to continue connecting'
		connStr = 'ssh -p' + str(self.port) + ' ' + self.user + '@' + self.host + ' -o PasswordAuthentication=' + self.pwdAuth
		try:
			child = pexpect.spawn(connStr)
			ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
			if ret == 0:
				print '[-] Error Connecting\n'
				return
			if ret == 1:
				child.sendline('yes')
				ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
				if ret == 0:
					print '[-] Error Connecting\n'
					return
			child.sendline(self.password)
			child.expect(PROMPT)
			return child
		except:
			return
		
	def send_command(self, cmd):
		session = self.connect()
		if session == None:
			return 
		session.sendline(cmd)
		session.expect(PROMPT)
		output = session.before
		session.close()
		return output
		
	def list(self, check_conn=False):
		if not check_conn:
			return self.host + ' ' + self.user
		session = self.connect()
		if session == None:
			return '[-] ' + self.host + ' ' + self.user
		return '[+] ' + self.host + ' ' + self.user
