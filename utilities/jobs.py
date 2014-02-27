import json
import time
import urllib2

from jsontools import read_json, write_json

#Utilities
def find_job(html, pos):
	"""find job id in html

	>>> html = '<div data-jobid="48374">'
	>>> find_job(html, 0)
	('48374', 5)
	>>> html = '<div></div>'
	>>> find_job(html, 0)
	('', -1)
	"""
	job = ''
	pos =  html.find("data-jobid", pos)
	if pos > -1:
		start = html.find('"', pos) + 1
		end = html.find('"', start)
		job = html[start:end]
	return job, pos

def get_tags(html):
	"""returns a list of tags from a html

	>>> html = '<p class="tags"><a class="post-tag job-link" href="/jobs/tag/java">java</a> \
	<a class="post-tag job-link" href="/jobs/tag/python">python</a> </p>'
	>>> get_tags(html)
	['java', 'python']
	"""
	end = 0
	tags = []
	for i in range(100):
		end = html.find("</a>", end)
		if end == -1:
			break
		start = html.rfind(">", 0, end)
		tag = html[start+1:end]
		tags.append(tag)

		end += 1

	return tags

def run():

	jobs = {}
	
	for page_number in range(1,54):
		#change 14 with error handling

		URL = "http://careers.stackoverflow.com/jobs?pg=" + str(page_number)
		print "Crunching page: ", page_number

		response = urllib2.urlopen(URL)
		html = response.read()

		#write html to file
		#f = open("jobs.txt", "w")
		#f.write(html)

		#process the file
		#file = "jobs.txt"
		#f = open("jobs.txt")
		#html = f.read()

		pos = -1
		#while(jp>=0):
		for i in range(100):

			job, pos = find_job(html, pos+1)
			#print pos
			
			#if we don't find a job
			if pos == -1:
				break

			if job not in jobs and job.isdigit():
				#move to a function to add tests
				tp_start = html.find('<p class="tags">', pos)
				tp_end = html.find("</p>", tp_start)
				string = html[tp_start:tp_end]
				tags = get_tags(string)
				jobs[job] = tags

		time.sleep(0.1)

	write_json("data/output.json", jobs)
	print "Total jobs crunched: ", len(jobs)

if __name__ == "__main__":
	run()
	import doctest
	doctest.testmod()
