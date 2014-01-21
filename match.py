import json

def generate_users():
	"""Get some users"""
	users = ["sajjad", "ari", "joakim"]
	interests = ["python", "machine learning", "debian", "prezi", "silly hardware"]
	dic = {"sajjad" : [1,1,0,1,0], "ari" : [1,1,1,1,0], "joakim" : [0,0,1,1,1] }
	f = open("users.json", "w")
	dic_json = json.dump(dic, sort_keys=True, indent=4, separators=(',', ': ') )
	f.write(dic_json)
	return dic