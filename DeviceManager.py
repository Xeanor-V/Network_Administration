
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pysnmp.entity.rfc3413.oneliner import ntforg
import os
import subprocess
import time
import datetime
import FileManager as FM
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntfrcv

def run_command(command):
	return subprocess.check_output(command, shell = true)

## Networks contains only the addresses 
def rip_configure(networks):
	config = "router rip\n"
	#run_command(config)
	for i in networks:
		config += "network " + i + "\n"
		#run_command(config)
	config += "exit"
	#run_command(config)
	return config

def ospf_configure(networks, routerID):
	config = "router ospf\n"
	#run_command(config)
	config += "router-id " + routerID + "\n"
	#run_command(config) 
	for i in networks:
		config += "network " + i[0] + " area " + str(i[1]) +"\n"
		#run_command(config)
	config +="exit\n" 
	run_command(config)
	return config

#EIGRP configuration :
##networks are subnet IDs networks = ['192.168.10','10.1.1.0']
def eigrp_configure(networks):
	config = "router eigrp\n"
	for i in networks:
		config += "network "+ i +"\n" # network 192.168.1.0 .YOU can use wildcard but that changes the networks structure
	config += "exit\n"
	run_command(config)
	return(config)	


#HSRP configuration (Host Standby Routing Protocol)
#virtual_gateway @ used by hosts as default gateway
#interface_id on which you will configure the HSRP: 'gi0/0'
#goup : vlan ID
#priority 110 by default .if you want to privilege a router just set the priority on a value > 110
#out_interface : 'se0/0/0'
#substrct_val : a substracted value fromm the priority of the active router
def hsrp_configure(virtual_gateway,interface_id,group , priority=110 , out_interface, substrct_val):
		config = "interface " + interface_id + "\n"
		config += "standby " + str(group) + " ip" + virtual_gateway + "\n"
		config += "standby " + str(group) + " priority " + str(priority) + "\n"
		#configure preemption when the active router is down :
		config += "standby " + str(group) + " preempt " + "\n"
		# if the out_interface is down :
		config += "standby " + str(group) + " track " + out_interface + str(substrct_val) + "\n"
		config += "exit\n"
		run_command(config)
		return(config)


def snmp_configure(community):
	s = "snmp-server community " + community
	#run_command(s)
	return s


def snmpget(ip,community,oid):
	s = "snmpget -v 2c -c " + community + " " + ip+ " " + oid
	return s
	#res = run_command(s)
	#print(res)

def save_config_tftp(ip,name):
	s  = "copy startup-config tfpt://"+ ip +"/"+ name
	return s
	#run_command(s)

def get_config_tfpt(ip,name):
	s = "copy ftp://" + ip + "/" + name +" startup-config"
	return s
	#run_command(s)

def get_Timestamp():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
	return st

# Callback function for receiving notifications
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
	s = 'Notification from ContextEngineId "%s", ContextName "%s"\n' % (contextEngineId.prettyPrint(),
	                                                      contextName.prettyPrint())
	print s

	for name, val in varBinds:
	    aux = '%s = %s\n' % (name.prettyPrint(), val.prettyPrint())
	    print(aux)
	    s += aux

	file = "System_log_" + get_Timestamp() + ".log"
	print "Trap recibido"
	print "Guardado en " + file 
	FM.write_file_str(file,s)



'''
snmptrap -v1 -c public 127.0.0.1 1.3.6.1.4.1.20408.4.1.1.2 127.0.0.1 1 1 123 1.3.6.1.2.1.1.1.0 s test
snmptrap -v2c -c public 127.0.0.1:162 123 1.3.6.1.6.3.1.1.5.1 1.3.6.1.2.1.1.5.0 s test
'''

def Trap_Listener():
	print("Escuchando traps")
	# Create SNMP engine with autogenernated engineID and pre-bound
	# to socket transport dispatcher
	snmpEngine = engine.SnmpEngine()

	# Transport setup

	# UDP over IPv4, first listening interface/port
	config.addTransport(
	snmpEngine,
	udp.domainName + (1,),
	udp.UdpTransport().openServerMode(('127.0.0.1', 162))
	)

	# UDP over IPv4, second listening interface/port
	config.addTransport(
	snmpEngine,
	udp.domainName + (2,),
	udp.UdpTransport().openServerMode(('127.0.0.1', 2162))
	)

	# SNMPv1/2c setup

	# SecurityName <-> CommunityName mapping
	config.addV1System(snmpEngine, 'my-area', 'public')


	# Register SNMP Application at the SNMP engine
	ntfrcv.NotificationReceiver(snmpEngine, cbFun)

	snmpEngine.transportDispatcher.jobStarted(1)  # this job would never finish

	# Run I/O dispatcher which would receive queries and send confirmations
	try:
		snmpEngine.transportDispatcher.runDispatcher()
	except:
		snmpEngine.transportDispatcher.closeDispatcher()
	raise


'''
 snmptrap -v2c -c public 127.0.0.1 0 SNMPv2-MIB::coldStart SNMPv2-MIB::sysName.0 = 'new name'
'''

def Send_Trap(comunity,target,MIB,symbol):
	ntfOrg = ntforg.NotificationOriginator()
	errorIndication = ntfOrg.sendNotification(
	    ntforg.CommunityData(comunity),
	    ntforg.UdpTransportTarget((target, 162)),
	    'trap',
	    ntforg.MibVariable(MIB, symbol),
	    ( ntforg.MibVariable(MIB, 'sysName', 0), 'new name' )
	)

	if errorIndication:
	    print('Notification not sent: %s' % errorIndication)


def store_device_info(deviceID):
	command = "dmidecode -t system"
	data = run_command(command)
	FM.write_file_str(deviceID + "_hardware.log",data)

def check_current_config(config,running):
	return FM.compare_files(config,ru)

##networks = ['10.0.0.0/24', '10.0.0.1/24']
##etworks = [ ['10.0.0.0/24',0] ,['10.0.0.1/24',0]]
##print ospf_configure(networks)

#Trap_Listener();# 
Send_Trap('public','127.0.0.1','SNMPv2-MIB','coldStart');


##file = "System_log_" + get_Timestamp() + ".log"
##print "Trap recibido Guardado en " + file 
#print(varBinds)
##FM.write_file_str(file,varBinds)