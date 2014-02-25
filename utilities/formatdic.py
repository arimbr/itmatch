import json
import operator
import time
from pythontools import read_json, write_json

file_name = "pythonjobs.json"
d = read_json(file_name)

#remove user withou categories
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
n = 20
popular_list = [c for c, p in popular][:n]
#print popular
print "The ", n, " most popular categories are:"
for p in popular_list:
	print p

#format jobs for ML
def format_data():
	data = {}
	for job, tags in d.iteritems():
		weights = dict(zip(popular_list, [0]*len(popular_list)))
		for tag in tags:
			if tag in popular_list:
				weights[tag] = 1

		data[job] = weights
	return data

data = format_data()
#print data


#Save data in json format
write_json("dm.json", data)





