command_center
==============

Python framework developed while reading <a href="http://www.amazon.com/Violent-Python-Cookbook-Penetration-Engineers/dp/1597499579" target="_blank">Violent Python: A Cookbook for Hackers, Forensic Analysts, Penetration Testers and Security Engineers</a> by T. J. O'Connor

You start by running the run.py which will take you to a "hub# " prompt.
From there on you have the following command list:

<pre>
list
	Description: lists all zombies inserted
			 -c/--check checks for connectivity
	usage: list [-c]

add
	Description: adds zombie host to botnet
	usage: add -h hostname -u user -p password -P <port>

remove
	Description: removes zombie host from botnet
	usage: remove -h hostname

broadcast
	Description: executes commands on all zombies
	usage: broadcast shell_command

execute
	Description: executes commandon spefic zombie
	usage: execute hostname shell_command

bruteforce
	Description: bruteforces SSH credentials on specific host
	usage: bruteforce [ --ssh -h hostname -u user -f dictionary [-p port] ]
					| [ --ssh -h hostname -u user --pub -D dir_with_keyfiles [-p port] ]
					| [ --zip -f zipfile -d dictionary ]
				
save
	Description: saves inserted zombies state into file state.vars
	usage: save

restore
	Description: restores previously inserted zombies from file state.vars
	usage: restore

shell
	Description: execute shell commands
	Usage: shell unix_command

help
	List available commands with "help" or detailed help with "help cmd".				

exit
	Exit the interpreter.
	You can also use the Ctrl-D shortcut
</pre>
<hr/>

The bruteforce command is designed most specifically for the <b>Debian weak private keys</b> issue discovered in 2008, or as the Violent Python book states:

<i>In 2006 something interesting happened with the Debian Linux Distribution. A developer commented on a line of code found by an automated software analysis toolkit. The particular line of code ensured entropy in the creation of SSH keys. By commenting on the particular line of code, the size of the searchable key space dropped to 15-bits of entropy (Ahmad, 2008). Without only 15-bits of entropy, this meant only 32,767 keys existed for each algorithm and size. HD Moore, CSO and Chief Architect at Rapid7, generated all of the 1024-bit and 2048 bit keys in under two hours (Moore, 2008). Moreover, he made them available for download at: http://digitaloffense.net/tools/debianopenssl/.  You  can  download  the  1024-bit  keys  to  begin.  After  downloading and extracting the keys, go ahead and delete the public keys, since we will only need the private keys to test our connection.</i>

The sources for the private/public keys are outdated though. But you can find them <a href="https://github.com/g0tmi1k/debian-ssh/tree/master/common_keys" target="_blank">here</a>


