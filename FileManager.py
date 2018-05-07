import filecmp

def write_file(filename, container):
	result_file  = open(filename, 'w')
	for key, value in container.iteritems():
		result_file.write(key + " " + value + '\n')
	result_file.close()
	
def compare_files(fileA, fileB):
	return filecmp.cmp(fileA,fileB)