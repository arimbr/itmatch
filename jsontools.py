def read_json(file_name):
	"""read json from a file and returns a python dictionary"""
	f = open(file_name)
	string = f.read()
	return json.loads(string)

def write_json(file_name, dic):
	"""write json into file from a python dictionary"""
	f = open(file_name, "w")
	dic_json = json.dumps(dic, separators=(',', ': ') )
	f.write(dic_json)
	f.close()