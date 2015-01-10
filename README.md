command_center
==============

Python framework developed while reading <a href="http://www.amazon.com/Violent-Python-Cookbook-Penetration-Engineers/dp/1597499579" target="_blank">Violent Python: A Cookbook for Hackers, Forensic Analysts, Penetration Testers and Security Engineers</a> by T. J. O'Connor

You start by running the run.py which will take you to a "hub# " prompt.
From there on you have the following command list:

<pre>
list
	Description: lists all zombies inserted
			 -c/--check checks for connectivity
	Usage: list [-c]

add
	Description: adds zombie host to botnet
	Usage: add -h &lt;hostname&gt; -u &lt;user&gt; -p &lt;password&gt; -P &lt;port&gt;

remove
	Description: removes zombie host from botnet
	Usage: remove -h &lt;hostname&gt;

broadcast
	Description: executes commands on all zombies
	Usage: broadcast &lt;shell command&gt;

execute
	Description: executes commandon spefic zombie
	Usage: execute &lt;hostname&gt; &lt;shell command&gt;

bruteforce
	Description: bruteforces SSH credentials on specific host
	Usage: bruteforce [ --ssh -h &lt;hostname&gt; -u &lt;user&gt; -f &lt;dictionary&gt; [-p &lt;port&gt;] ]
					| [ --ssh -h &lt;hostname&gt; -u &lt;user&gt; --pub -D &lt;dir with keyfiles&gt; [-p &lt;port&gt;] ]
					| [ --zip -f &lt;zipfile&gt; -d &lt;dictionary&gt; ]

openrelay
	Description: tests if a server is configured to relay emails coming from anywhere
	Usage: openrelay -f &lt;sender email address&gt; -t &lt;receiver email address&gt; -s &lt;mail server&gt; -p &lt;port&gt;
				
save
	Description: saves inserted zombies state into file state.vars
	Usage: save

restore
	Description: restores previously inserted zombies from file state.vars
	Usage: restore

shell
	Description: execute shell commands
	Usage: shell &lt;unix command&gt;

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


