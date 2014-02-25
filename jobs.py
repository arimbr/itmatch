import json
import time
import urllib2

#Utilities
def find_job(html, jp):
	jp =  html.find("jobid", jp)
	job = html[jp + 7:html.find('"', jp+8)]
	return job, jp + 1

def get_tags(string):
	"""'<p class="tags"><a class="post-tag job-link" href="/jobs/tag/java">java</a> <a class="post-tag job-link"
	href="/jobs/tag/c%2b%2b">c++</a> <a class="post-tag job-link" href="/jobs/tag/c">c</a>
	<a class="post-tag job-link" href="/jobs/tag/python">python</a> </p>'"""
	end = 0
	tags = []
	for i in range(100):
		end = string.find("</a>", end)
		if end == -1:
			break
		start = string.rfind(">", 0, end)
		tag = string[start+1:end]
		tags.append(tag)

		end += 1

	return tags

def write_json(file_name, dic):
	"""write json into file from a python dictionary"""
	f = open(file_name, "w")
	dic_json = json.dumps(dic, separators=(',', ': ') )
	f.write(dic_json)
	f.close()

jobs = {}

for page_number in range(1,14):
	#change 14 with error handling
	print "Crunching page: ", page_number

	URL = "http://careers.stackoverflow.com/jobs?searchTerm=python&pg=" + str(page_number)

	response = urllib2.urlopen(URL)
	html = response.read()

	#write html to file
	#f = open("jobs.txt", "w")
	#f.write(html)

	#process the file
	#file = "jobs.txt"
	#f = open("jobs.txt")
	#html = f.read()

	jp = 0
	#while(jp>=0):
	for i in range(100):

		job, jp = find_job(html, jp)
		if jp == -1:
			break

		if job not in jobs and len(job) < 10: #change for job contains only digits
			tp_start = html.find('<p class="tags">', jp)
			tp_end = html.find("</p>", tp_start)
			string = html[tp_start:tp_end]
			tags = get_tags(string)
			jobs[job] = tags

	time.sleep(1)



write_json("pythonjobs.json", jobs)
print "Total jobs crunched: ", len(jobs)
