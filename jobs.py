import json
import time
import urllib2

from jsontools import read_json, write_json

#Utilities
def find_next_job(html, p):
	"""Returns job id and position in a html string

	>>> html = '<div data-jobid="48374">'
	>>> find_next_job(html, 0)
	('48374', 6)
	"""
	job_pos =  html.find("data-jobid", p)
	start = html.find('"', job_pos)
	end = html.find('"', start + 1)
	job_id = html[start + 1:end]
	return job_id, job_pos + 1

def get_tags(string):
	"""'<p class="tags"><a class="post-tag job-link" href="/jobs/tag/java">java</a> \
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

def run():
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

			job, jp = find_next_job(html, jp)
			if jp == -1:
				break

			if job not in jobs and len(job) < 10: #change for job contains only digits
				tp_start = html.find('<p class="tags">', jp)
				tp_end = html.find("</p>", tp_start)
				string = html[tp_start:tp_end]
				tags = get_tags(string)
				jobs[job] = tags

		time.sleep(1)


jobs = {}

run()
#write_json("pythonjobs.json", jobs)
#print "Total jobs crunched: ", len(jobs)

if __name__ == "__main__":
	import doctest
	doctest.testmod()
