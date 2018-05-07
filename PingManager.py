import os
import subprocess
import pingparser
import nmap
import ErrorManager as ErrorM
from collections import OrderedDict


def make_ping(hostname, number = 3):
	try:
		output = subprocess.check_output("ping -c " + str(number) + " " + hostname, shell=True)
		results = pingparser.parse(output)

	except Exception as e:
		ErrorM.send_email('vg.ursa@gmail.com', hostname + ' not responding')
		results = {}
		results["host"] = hostname
		results["received"] = '0'
		results["sent"] = '5' 
		results["jitter"] = '0'
		results["packet_loss"] = '0'
		results["avgping"] = '0'
		results["minping"] = '0'
		results["maxping"] = '0'	 

	return OrderedDict(sorted(results.items()))



def find_hosts():
	nm = nmap.PortScanner()
	nm.scan(hosts='192.168.0.0/24', arguments='-n -sP -PE -PA21,23,80,3389')
	hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
	for host, status in hosts_list:
		print('{0}:{1}'.format(host, status))