import json
from random import random as random

users = ["sajjad", "ari", "joakim"]
interests = ["python", "machine learning", "debian", "prezi", "silly hardware"]
dic = {"sajjad" : [1,1,0,1,0], "ari" : [1,1,1,1,0], "joakim" : [0,0,1,1,1] }

def generate_users(dic):
	"""Get some users"""
	file_name = "users.json"
	write_json(file_name, dic)

def read_json(file_name):
	"""read json from a file and returns a python dictionary"""
	f = open(file_name)
	string = f.read()
	return json.loads(string)

def write_json(file_name, dic):
	"""write json into filqe from a python dictionary"""
	f = open(file_name, "w")
	dic_json = json.dumps(dic, separators=(',', ': ') )
	f.write(dic_json)
	f.close()

def get_weight(m=5, treshold=0.5):
	"""returns a list with random 0s and 1s"""
	weight = []
	for i in range(m):
		num = random()
		if num < treshold:
			weight.append(1)
		else:
			weight.append(0)
	return weight

def get_weights(n=3, m=5, treshold=0.5):
	"""Returns a list of lists with random 0s and 1s"""
	weights = []
	for i in range(n):
		weight = get_weight(m, treshold)
		weights.append(weight)
	return weights

def get_readable(users=users, interests=interests):
	"""returns a dictionary where the keys are dictionaries"""
	weights = get_weights();
	return dict(zip(users, [dict(zip(interests, weight)) for weight in weights]))