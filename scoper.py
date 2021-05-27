# last updated: 2021-05-27

import json
import re
import sys
from urllib.parse import urlparse

class tcol:
	'''tcol: contains terminal color codes; always close a colorized string by appending "tcol.RESET"'''
	GREEN = '\033[92m'
	RED = '\033[91m'
	RESET = '\033[0m'

class ScoperCore:
	def __init__(self, config="", url="", urls=[]):
		'''__init__: provide a Burp configuration and a single URL or list of URLs to check'''
		self.config = config
		if type(self.config).__name__ == "str": # if provided a path to the burp config
			with open(self.config, "r") as cnf:
				self.conf = json.load(cnf)
			cnf.close()
		elif type(self.config).__name__ == "dict": # if directly provided the burp config as a dict
				self.conf = self.config
		self.url = url # provided string
		self.urls = urls # provided list

	def processUrl(self, conf, clude, url):
		'''processUrl(): checks provided URL against the "include" and "exclude" sections of the Burp configuration file; returns the same URL if it meets the criteria, otherwise it returns an empty string'''
		url = url.strip()
		urlp = urlparse(url)
		u = urlp.netloc # domain portion of URL
		if urlp.port:
			u = u.split(":")[0]
			pt = str(urlp.port) # port is checked as a regex string in the Burp config
		else:
			if "http://" in url:
				pt = "80"
			elif "https://" in url:
				pt = "443"
		p = urlp.path # path portion of URL
		s = urlp.scheme # http/https portion of URL
		if len(p) == 0:
			p = "/"
		if len(s) == 0:
			s = "https" # default to HTTPS
		if clude in conf["target"]["scope"]:
			for x in conf["target"]["scope"][clude]:
				#
				#
				# track a pass/fail score; unanimous assessment required for result
				score = []
				if "protocol" in x:
					if x["protocol"] != s:
						#print("FAILED PROTOCOL CHECK:", clude, s, "requires:", x["protocol"], "\t\t\t\turl:", url)
						#return("")
						score.append("fail")
					else:
						score.append("pass")
				if "host" in x:
					if not re.match(x["host"], u, re.DOTALL):
						#print("FAILED HOST CHECK:", clude, u, "requires:", x["host"], "\turl:", url)
						#return("")
						score.append("fail")
					else:
						score.append("pass")
				if "file" in x: # burp file = url path
					if not re.match(x["file"], p, re.DOTALL):
						#print("FAILED FILE CHECK:", clude, p, "requires:", x["file"], "\t\t\turl:", url)
						#return("")
						score.append("fail")
					else:
						score.append("pass")
				if "port" in x:
					if not re.match(x["port"], pt, re.DOTALL):
						#print("FAILED PORT CHECK:", clude, pt, "requires:", x["port"], "\t\t\t\t\turl:", url)
						#return("")
						score.append("fail")
					else:
						score.append("pass")
				#
				#
				# check the score
				#
				# include pass = is included
				# include fail = is not included (so "not" this condition / all passes = hit)
				# exclude fail = is included (so "not" this condition / all passes = hit)
				# exclude pass = is not included
				#
				if "fail" not in score:
					return(url)
				else:
					pass
		return("") # pending all checks and no results, fail closed

	def __repr__(self):
		'''__repr__(): returns the result'''
		return(self.output)

class ScoperSingle(ScoperCore):
	def __init__(self, config="", url="", urls=[]):
		'''__init__: initialize variables to check a single URLs'''
		super().__init__(config, url, urls) # inherit from ScoperCore
		self.output = {}
		self.check() # populates self.output
		self.json = json.dumps(self.output)
		self.color() # sets self.color

	def check(self):
		'''check(): compares the input URL to the include/exclude logic, and determines if the URL is in scope or not'''
		i = self.processUrl(self.conf, "include", self.url)
		if len(i) > 0:
			e = self.processUrl(self.conf, "exclude", i)
			if i != e:
				self.output = {'scope':'inside', 'url':i}
			else:
				self.output = {'scope':'outside', 'url':i}
		else:
			self.output = {'scope':'outside', 'url':self.url} # default to outside as a precaution

	def color(self):
		'''color(): sets self.color as a colorized string representation of self.output'''
		if "scope" in self.output:
			if self.output["scope"] == "inside":
				self.color = str(tcol.GREEN+"scope-inside"+tcol.RESET+"\t"+self.output["url"])
			if self.output["scope"] == "outside":
				self.color = str(tcol.RED+"scope-outside"+tcol.RESET+"\t"+self.output["url"])

class ScoperList(ScoperCore):
	def __init__(self, config="", url="", urls=[]):
		'''__init__: initialize variables to check a list of URLs'''
		super().__init__(config, url, urls) # inherit from ScoperCore
		self.output = {'scope':{'inside':[], 'outside':[]}}
		self.check() # populates self.output
		self.json = json.dumps(self.output)
		self.color = self.color()

	def check(self):
		'''check(): compares the input URL to the include/exclude logic, and determines if the URL is in scope or not'''
		for url in self.urls:
			i = self.processUrl(self.conf, "include", url)
			if len(i) > 0:
				e = self.processUrl(self.conf, "exclude", i)
				if i != e:
					self.output['scope']['inside'].append(i)
				else:
					self.output['scope']['outside'].append(i)
			else:
				self.output['scope']['outside'].append(url) # default to outside as a precaution

	def color(self):
		'''color(): sets self.color as a colorized string representation of self.output'''
		cc = ""
		for i in self.output['scope']['inside']:
			cc += str(tcol.GREEN+"scope-inside"+tcol.RESET+"\t"+i+"\n")
		for i in self.output['scope']['outside']:
			cc += str(tcol.RED+"scope-outside"+tcol.RESET+"\t"+i+"\n")
		return(cc)

	def output_generator(self):
		'''output_generator(): this generator function produces output similar to ScoperSingle, ex. {'scope':'inside', 'url':'xyz'} for sake of consistency'''
		t = []
		for i in self.output['scope']['inside']:
			t.append({'scope':'inside', 'url':i})
		for i in self.output['scope']['outside']:
			t.append({'scope':'outside', 'url':i})
		for x in t:
			yield(x)

	def json_generator(self):
		'''json_generator(): generator function uses output_generator() to dump JSON strings like ScoperSingle, ex. {"scope":"inside", "url":"xyz"} for sake of consistency'''
		for i in self.output_generator():
			yield(json.dumps(i))
