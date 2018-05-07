import os
import subprocess
import time

##Date should be in seconds
def create_database(dbname, date, variable):
	command = 'rrdtool create '  + dbname + '.rrd --start '  + str(date);
	command += ' DS:' + variable + ':COUNTER:600:U:U'
	command +=' RRA:AVERAGE:0.5:1:24'
	print command;
	os.system(command)

def update_database(dbname, time, value):
	command = 'rrdtool update ' + dbname + ' ' + str(time) + ':' + str(value)
	print command
	os.system(command)

def fetch_database(dbname, start, end):
	command = 'rrdtool fetch ' + dbname +  ' AVERAGE --start ' + str(start) + ' --end ' + str(end)
	print command
	os.system(command)

def graph_database(dbname, outname, variable, start, end):
	command = 'rrdtool graph ' + outname + '.png --start ' + str(start) + ' --end ' + str(end)
	command += ' DEF:' + dbname.split('.')[0] + '=' + dbname + ':' + variable + ':AVERAGE'
	command += ' LINE2:'+ dbname.split('.')[0]+ '#FF0000'
	print command
	os.system(command)







##create_database('Test', epoch,'pingMax')
##update_database('Test.rrd', 1521089000, 4)
##fetch_database('Test.rrd', 1521089000, 1521089900)
##graph_database('Test.rrd', 'pingMax', 'pingMax', 1521089000, 1521089900)


