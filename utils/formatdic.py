import json
import operator
import time

from jsontools import read_json, write_json

data = read_json("data/jobs.json")

print "Before cleaning there are ", len(data), " jobs"

#get tags frequencies
def get_tags_frequencies(data):
	frequency = {}
	for job, tags in data.iteritems():
		for tag in tags:
			if tag not in frequency:
				frequency[tag] = 1
			else:
				frequency[tag] += 1
	return frequency

def filter_tags(d, tags):
	"""
	Takes out values from d that are not in tags, and also users that have no tags
	"""
	return dict([(k,filter(lambda x: x in tags, v))
				for k, v in d.iteritems() if v])

def clean_empty_values(d):
	return dict([(k, v) for k,v in d.iteritems() if len(v)>0][:20])	


tags = get_tags_frequencies(data)
print "There are ", len(tags), " tags"
print "\n"

# -------- Start to refactor ---------

popular = sorted(tags.iteritems(), key=operator.itemgetter(1), reverse=True) #list of tuples
popularity_threshold = 120
popular_tags = [(c, p) for c, p in popular if p > popularity_threshold]
#print popular
print "There are " + str(len(popular_tags)) + " tags with more than " + str(popularity_threshold) + " users"

for c, p in popular_tags:
	print p, c

tags = [c for c, _ in popular_tags]
write_json("data/tags_output.json", tags)
print "Writing tags to tags.json"

# --------- End to refactor ------

data = filter_tags(data, tags)
data = clean_empty_values(data)
print "After cleaning there are ", len(data), "jobs"

write_json("data/users_output.json", data)

if __name__ == "__main__":
	import doctest
	doctest.testmod()




