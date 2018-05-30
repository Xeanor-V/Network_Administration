import getpass
import sys
import telnetlib



def run_telnet(host, user, password, commandos):

	HOST = host #"localhost"
	user = user #raw_input("Enter your remote account: ")
	password = password #getpass.getpass()

	tn = telnetlib.Telnet(HOST)

	tn.read_until("login: ")
	tn.write(user + "\n")
	if password:
	    tn.read_until("Password: ")
	    tn.write(password + "\n")

	comand = commandos.split('\n')
	for c in commandos:
		s = c + '\n'
		tn.write(s)
	tn.write("exit\n")
	return tn.read_all()