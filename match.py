import json
from random import random as random
import sys

#users = ['U'+str(i) for i in range(10)]
#categories = ['C'+str(i) for i in range(10)]

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

def get_weights(m=10, n=10, threshold=0.7):
	"""Returns a list of lists with random 0s and 1s"""
	weights = []
	for i in range(m):
		weight = []
		for i in range(n):
			if random() < threshold:
				weight.append(1)
			else:
				weight.append(0)
		weights.append(weight)
	return weights

def get_data(m=8, n=8):
	#we may run out of memory for m,n = 10, 10 !!!!
	"""returns a dictionary with users as keys
	and dictionaries as values"""
	users = ['U'+str(i) for i in range(m)]
	categories = ['C'+str(i) for i in range(n)]
	weights = get_weights(m, n);
	return dict(zip(users, [dict(zip(categories, weight))
							for weight in weights]))

def intersection(data, user1, user2):
	"""returns a number between 0.0 and 1.0"""
	"""0 for for nothing in common, 1 for all ones vector"""
	v1 = data[user1]
	v2 = data[user2]
	sum = 0.0
	for key in v1:
		sum = sum + v1[key]*v2[key]

	return sum/len(v1)

def tanimoto(data, user1, user2):
	"""returns a number between 0.0 and 1.0
	0.0 nobody who wants the first item wants the second one,
	and 1.0 means that v1 and v2 are equal"""

	v1 = data[user1]
	v2 = data[user2]
	c1, c2, shr = 0, 0, 0
	for c in v1:
		if v1[c]!=0: c1 += 1  # in v1
		if v2[c]!=0: c2 += 1  # in v2
		if v1[c]!=0 and v2[c]!=0: shr += 1  # in both
	try:
		return float(shr)/(c1 + c2 - shr)
	except ZeroDivisionError:
		return 0

def top_matches(data, user, n=5, distance=tanimoto):
	"""returns the best n matches for user as a list of tuples"""
	scores = [(distance(data, user, other), other)
				for other in data if other!=user]
	scores.sort()
	scores.reverse()
	return scores[0:n]

def distance_matrix(data, distance=tanimoto):
	dm = {} #optimize
	for user1 in data:
		dm[user1] = {}
		for user2 in data:
			dm[user1][user2] = tanimoto(data, user1, user2)
	return dm

if __name__ == '__main__':
	"""command line app, usage: python match.py U1"""
	user = sys.argv[1]
	data = get_data()
	print top_matches(data, user)