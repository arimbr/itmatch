import json
import sys

from random import random as random

from jsontools import read_json, write_json

def tanimoto(data, user1, user2):
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
		return 1.0

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

def top_matches(data, user, n=5, distance=tanimoto):
	#should be done from distance_matrix lookup
	"""returns the best n matches for user as a list of tuples"""
	scores = [(distance(data, user, other), other)
				for other in data if other!=user]
	scores.sort()
	return scores[0:n]

if __name__ == '__main__':
	import doctest
	doctest.testmod()
