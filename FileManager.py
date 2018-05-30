import filecmp
import ErrorManager as ERM

def write_file_dic(filename, container):
	result_file  = open(filename, 'w')
	for key, value in container.iteritems():
		result_file.write(key + " " + value + '\n')
	result_file.close()

def write_file_obj(filename,obj):
	result_file  = open(filename, 'w')
	for value in obj:
		res = "%s" % value
		result_file.write(res)
	result_file.close()

def write_file_str(filename,string):
	result_file  = open(filename, 'w')
	result_file.write(string)
	result_file.close()


def read_file(filename):
	res = ""
	file = open(filename, 'r')
	for line in file:
		res += line
	return res

def check_log(filename,errors):
	file = open(filename, 'r')
	res = []
	for line in file:
		for error in errors
			if error in line:
				res.append(error)
	return res



	
def compare_files(fileA, fileB):
	return filecmp.cmp(fileA,fileB)


file = "System_log_2018_05_30_01_12_40.log"
errors = ["1.3.6.1.6.3.1.1.4.1.0"]
if(check_log(file,errors)):
	ERM.send_email("vg.ursa@gmail.com",read_file(file))

