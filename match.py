import json
from random import random as random
import sys

#users = ['U'+str(i) for i in range(n)]
#categories = ['C'+str(i) for i in range(m)]

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

def get_weight(n=10, threshold=0.7):
	"""returns a list with random 0s and 1s"""
	weight = []
	for i in range(n):
		num = random()
		if num < threshold:
			weight.append(1)
		else:
			weight.append(0)
	return weight

def get_weights(m=10, n=10):
	"""Returns a list of lists with random 0s and 1s"""
	weights = []
	for i in range(m):
		weight = get_weight(n)
		weights.append(weight)
	return weights

def get_data(m=10, n=10):
	"""returns a dictionary where the keys are dictionaries"""
	users = ['U'+str(i) for i in range(m)]
	categories = ['C'+str(i) for i in range(n)]
	weights = get_weights(m, n);
	return dict(zip(users, [dict(zip(categories, weight)) for weight in weights]))

def dist(data, user1, user2):
	#v is dictionary with the categories
	v = data[user1]
	w = data[user2]
	sum = 0.0
	for key in v:
		sum = sum + v[key]*w[key]

	return sum/len(v)

def compare(j,k):
	data = get_data()
	v, w = data[j], data[k]
	return dist(v, w)

def topMatches(data, user, n=5, similarity=dist):
	"""returns the best matches for user"""
	scores = [(similarity(data, user, other), other)
				for other in data if other != user]
	scores.sort()
	scores.reverse()
	return scores[0:n]


if __name__ == '__main__':
	"""command line app"""
	user = sys.argv[1]
	print user
	data = get_data()
	tp = topMatches(data, user)
	print tp



