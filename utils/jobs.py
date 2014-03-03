import json
import time
import urllib2
import os.path

from jsontools import read_json, write_json

BASE_URL = "http://careers.stackoverflow.com/jobs?pg="
JOBS_FILE = os.path.dirname(os.path.abspath(__file__)) + '/data/jobs.json'
print JOBS_FILE

def get_job(html, pos):
	"""find job id in html

	>>> html = '<div data-jobid="48374">'
	>>> get_job(html, 0)
	('48374', 5)
	>>> html = '<div></div>'
	>>> get_job(html, 0)
	('', -1)
	"""
	job = ''
	pos =  html.find("data-jobid", pos)
	if pos > -1:
		start = html.find('"', pos) + 1
		end = html.find('"', start)
		job = html[start:end]
	return job, pos

def get_tags_html(html, pos):
	"""
	>>> html = '<div data-jobid="44623" class="highlighted"><p class="posted top">&lt; 1 hour ago</p><p class="tags"><a class="post-tag job-link" href="/jobs/tag/java">java</a><a class="post-tag job-link" href="/jobs/tag/python">python</a> </p> <p></p>'
	>>> get_tags_html(html, 0)
	'<p class="tags"><a class="post-tag job-link" href="/jobs/tag/java">java</a><a class="post-tag job-link" href="/jobs/tag/python">python</a> </p>'
	"""
	start = html.find('<p class="tags">', pos)
	end = html.find("</p>", start) + len("</p>")
	return html[start:end]

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

def crunch():
	"""
	Update jobs.json with new jobs
	"""

	jobs = read_json(JOBS_FILE)
	jobs_length_before = len(jobs)

	for page_number in range(1,100):

		URL = BASE_URL + str(page_number)
		
		print "Crunching page: ", page_number
		response = urllib2.urlopen(URL)
		html = response.read()

		# break if page has no jobs
		job, pos = get_job(html, 0)
		if pos == -1:
			break

		#get jobs and tags
		pos = -1
		for i in range(100):

			#if we don't find a job
			job, pos = get_job(html, pos+1)
			if pos == -1:
				break

			if job not in jobs and job.isdigit():
				#move to a function to add tests
				tags_html = get_tags_html(html, pos)
				tags = get_tags(tags_html)
				jobs[job] = tags

		time.sleep(0.5)

	jobs_length_after = len(jobs)
	print "Number of jobs added: ", jobs_length_after - jobs_length_before
	print "Total number of jobs: ", jobs_length_after
	print "Writing jobs in: ", JOBS_FILE
	write_json(JOBS_FILE, jobs)

if __name__ == "__main__":
	crunch()
	import doctest
	doctest.testmod()
