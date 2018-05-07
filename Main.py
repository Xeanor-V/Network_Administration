import FileManager as FileM
import DeviceManager as DevM
import DatabaseManager as DataM
import PingManager as PingM
import ErrorManager as ErrorM

## epoch = int(time.time()) gets the seconds since the unix timestamp

if __name__ == "__main__":
	print "IP/Hostname: "
	hostname = raw_input() 
	FileM.write_file('ping_result.txt', PingM.make_ping(hostname,3))


##PingM.find_hosts();