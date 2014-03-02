import json
import sys
from random import random as random
from jsontools import read_json, write_json

#users = ['U'+str(i) for i in range(10)]
#categories = ['C'+str(i) for i in range(10)]

def get_weights(m=10, n=10, threshold=0.7):
	"""Returns a list of lists with random 0s and 1s
	>>> type(get_weights())
	<type 'list'>
	>>> len(get_weights())
	10
	>>> len(get_weights()[0])
	10
	"""
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
	and dictionaries as values
	"""
	users = ['U'+str(i) for i in range(m)]
	categories = ['C'+str(i) for i in range(n)]
	weights = get_weights(m, n);
	return dict(zip(users, [dict(zip(categories, weight))
							for weight in weights]))

def intersection(data, user1, user2):
	"""returns a number between 0.0 and 1.0
	0 for for nothing in common, 1 for all ones vector"""
	v1 = data[user1]
	v2 = data[user2]
	sum = 0.0
	for key in v1:
		sum = sum + v1[key]*v2[key]

	return sum/len(v1)

def tanimoto(data, user1, user2):
	"""returns a number between 0.0 and 1.0
	0.0 nobody who wants the first item wants the second one,
	and 1.0 means that v1 and v2 are equal
	"""
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

def tanimoto2(data, user1, user2):
	"""returns the distance between user1 and user2
	0.0 means that the users tags are equal
	1.0 means that the user don't have any tag in common
	data is a dictionary whith user ids as key, and a list of tags as values
	user1 and user2 are user ids

	>>> data = {'1': ["python", "C"], '2': ["python", "C"]}
	>>> tanimoto2(data, '1', '2')
	0.0
	>>> data = {'1': ["python", "C"], '2' : ["java"]}
	>>> tanimoto2(data, '1', '2')
	1.0
	>>> data = {'1': ["python", "C"], '2': ["python"]}
	>>> 0 < tanimoto2(data, '1', '2') < 1
	True
	>>> data = {'1': [], '2': []}
	>>> tanimoto2(data, '1', '2')
	1.0
	"""
	v1 = data[user1]
	v2 = data[user2]

	c1 = len(v1)
	c2 = len(v2)
	shr = len(set(v1).intersection(v2))
	try:
		return 1 - float(shr)/(c1 + c2 - shr)
	except ZeroDivisionError:
		#v1 and v2 empty lists	
		#print user1, v1, c1
		#print user2, v2, c2
		#print "*"*10
		return 1.0
	


def top_matches(data, user, n=5, distance=tanimoto):
	"""returns the best n matches for user as a list of tuples"""
	scores = [(distance(data, user, other), other)
				for other in data if other!=user]
	scores.sort()
	scores.reverse()
	return scores[0:n]

def distance_matrix(data, distance=tanimoto):
	"""returns a square symmetric matrix with
	the distances between each pair of users
	"""
	dm = {} #optimize
	for user1 in data:
		dm[user1] = {}
		for user2 in data:
			dm[user1][user2] = distance(data, user1, user2)
	return dm

if __name__ == '__main__':
	"""command line app, usage: python match.py U1"""
	#user = sys.argv[1]
	#data = get_data()
	#print top_matches(data, user)

	import doctest
	doctest.testmod()
