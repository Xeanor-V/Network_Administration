import os
import subprocess

def run_command(command):
	return subprocess.check_output(command, shell = true)

## Networks contains only the addresses 
def rip_configure(networks):
	config = "router rip\n"
	for i in networks:
		config += "network " + i + "\n"
	config+= "exit\n"
	return config

def ospf_configure(networks):
	config = "router ospf\n"
	for i in networks:
		config += "network " + i[0] + " area " + str(i[1]) +"\n";
	config+="exit\n" 
	return config

def snmp_configure(community):
	return "snmp-server community " + community

def snmp_get(ip,community,oid):
	return "snmpget -v 2c -c " + community + " " + ip+ " " + oid

def save_config_tftp(ip,name):
	return "copy startup-config tfpt://"+ ip +"/"+ name

def get_config_tfpt(ip,name):
	return "copy tftp://" + ip + "/" + name +" startup-config"
	 


##networks = ['10.0.0.0/24', '10.0.0.1/24']
networks = [ ['10.0.0.0/24',0] ,['10.0.0.1/24',0]]
print ospf_configure(networks)
