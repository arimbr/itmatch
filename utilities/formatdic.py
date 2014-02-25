import json
import operator
import time

from jsontools import read_json, write_json

file_name = "data/output.json"
d = read_json(file_name)

#remove user without categories
print "Before cleaning there are ", len(d), " jobs"
empty_jobs = []
for job, tags in d.iteritems():
	if len(tags) == 0:
		empty_jobs.append(job)

for job in empty_jobs:
	del d[job]

print "After cleaning there are ", len(d), " jobs"

#get categories frequencies
categories = {}
for job, tags in d.iteritems():
	for tag in tags:
		if tag not in categories:
			categories[tag] = 1
		else:
			categories[tag] += 1


print "There are ", len(categories), " categories"
print "\n"
time.sleep(3)

popular = sorted(categories.iteritems(), key=operator.itemgetter(1), reverse=True) #list of tuples
popularity_threshold = 10
popular_categories = [c for c, p in popular if p > popularity_threshold]
#print popular
print "There are " + str(len(popular_categories)) + " categories with more than " + str(popularity_threshold) + " users"
for p in popular_categories:
	print p
write_json("data/categories.json", popular_categories)
print "writing categories in json format to categories.json"

#format jobs for ML
def format_data():
	data = {}
	for job, tags in d.iteritems():
		weights = dict(zip(popular_categories, [0]*len(popular_categories)))
		for tag in tags:
			if tag in popular_categories:
				weights[tag] = 1

		data[job] = weights
	return data

data = format_data()
#print data
#Format data so we dont have users without categories

def more_than_n_non_zero_values(dic, n):
	count = 0
	for k, v in dic.iteritems():
		if v != 0:
			count += 1
	if count > n:
		return True
	else:
		return False

print "lenght of data before cleaning: ", len(data)

"""Clean data"""
clean_data = {}
n = 4
for job, tags in data.iteritems():
	if more_than_n_non_zero_values(tags, n):
		clean_data[job] = tags

print "length of data after cleaning: ", len(clean_data)

#Save data in json format
write_json("data/output.json", clean_data)





