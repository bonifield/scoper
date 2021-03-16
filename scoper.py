# last updated: 2021-03-16

import json, re
from urllib.parse import urlparse

class tcol:
	'''tcol: contains terminal color codes; always close a colorized string by appending "tcol.RESET"'''
	PURPLE = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	RESET = '\033[0m'

class ScoperList:
	def __init__(self, conf, inputUrls, output=None):
		'''__init__: provide a Burp configuration and a list of URLs to check'''
		self.conf = conf
		self.inputUrls = inputUrls

	def processIncludes(self, conf, inputUrls):
		'''processIncludes(): checks provided URLs against the "include" section of the Burp configuration file; returns a list of URLs to include, as a subset of the original input list'''
		includeUrls = []
		for i in inputUrls:
			u = urlparse(i).netloc # domain portion of URL
			if "http://" in i:
				h = "http"
			if "https://" in i:
				h = "https"
			for x in conf["target"]["scope"]["include"]:
				if x["protocol"] == h:
					y = re.match(x["host"], u, re.DOTALL)
					if y:
						includeUrls.append(i)
		return(list(set(includeUrls)))

	def processExcludes(self, conf, includeUrls):
		'''processExcludes(): checks provided URLs against the "exclude" section of the Burp configuration file; returns a list of URLs to exclude, as a subset of the original input list'''
		excludeUrls = []
		for i in includeUrls:
			u = urlparse(i).netloc # domain portion of URL
			p = urlparse(i).path # path portion of URL
			if len(p) == 0:
				p = "/"
			if "http://" in i:
				h = "http"
			if "https://" in i:
				h = "https"
			for x in conf["target"]["scope"]["exclude"]:
				if x["protocol"] == h:
					y = re.match(x["host"], u, re.DOTALL)
					z = re.match(x["file"], p, re.DOTALL)
					if y:
						if z:
							excludeUrls.append(i)
		return(list(set(excludeUrls)))

	def check(self):
		'''check(): subtracts the excludel list from the include list to drop any conflicting items; returns a final list of only in-scope items'''
		i = self.processIncludes(self.conf, self.inputUrls)
		e = self.processExcludes(self.conf, i)
		o = list(set(i) - set(e))
		self.output = o
		return(o)

	def gen(self):
		'''gen(): a generator object for the results list, accessible after Scoper.check() has been run'''
		for i in self.output:
			yield(i)

	def colors(self):
		'''colors(): a generator object for the results list that yields the result with colorized strings'''
		for i in self.output:
			yield(tcol.GREEN+"inside-scope"+tcol.RESET+"\t"+i)

	def json(self):
		'''json(): a generator object for the results list that yields the result in JSON'''
		for i in self.output:
			y = json.dumps({"scope":"inside", "host":i})
			yield(y)

	def __repr__(self):
		'''__repr__(): returns the results list, one item per line (newline-delimited)'''
		o = self.check()
		self.output = o
		return("\n".join(o))

class ScoperSingle:
	def __init__(self, conf, inputUrl, output=""):
		'''__init__: provide a Burp configuration and a single URL to check'''
		self.conf = conf
		self.inputUrl = inputUrl
		self.output = ""

	def processIncludes(self, conf, inputUrl):
		'''processIncludes(): checks provided URL against the "include" section of the Burp configuration file; returns a the same URL if it meets the include criteria, otherwise it returns an empty string'''
		inputUrl = inputUrl.strip()
		includeUrl = ""
		u = urlparse(inputUrl).netloc # domain portion of URL
		if "http://" in inputUrl:
			h = "http"
		if "https://" in inputUrl:
			h = "https"
		for x in conf["target"]["scope"]["include"]:
			if x["protocol"] == h:
				y = re.match(x["host"], u, re.DOTALL)
				if y:
					includeUrl = inputUrl
		return(includeUrl)

	def processExcludes(self, conf, includeUrl):
		'''processExcludes(): checks provided URL against the "exclude" section of the Burp configuration file; returns a the same URL if it meets the exclude criteria, otherwise it returns an empty string'''
		includeUrl = includeUrl.strip()
		excludeUrl = ""
		u = urlparse(includeUrl).netloc # domain portion of URL
		p = urlparse(includeUrl).path # path portion of URL
		if len(p) == 0:
			p = "/"
		if "http://" in includeUrl:
			h = "http"
		if "https://" in includeUrl:
			h = "https"
		for x in conf["target"]["scope"]["exclude"]:
			if x["protocol"] == h:
				y = re.match(x["host"], u, re.DOTALL)
				z = re.match(x["file"], p, re.DOTALL)
				if y:
					if z:
						excludeUrl = includeUrl
		return(excludeUrl)

	def check(self):
		'''check(): compares the input URL to the include/exclude logic, and determins if the URL is in scope or not'''
		i = self.processIncludes(self.conf, self.inputUrl)
		if len(i) > 0:
			e = self.processExcludes(self.conf, i)
			if i != e:
				self.output = "inside-scope\t"+i
			else:
				self.output = "outside-scope\t"+i
			return(self.output)
		else:
			self.output = "outside-scope\t"+self.inputUrl
		return(self.output)

	def colors(self):
		'''colors(): returns the result with colorized output'''
		cc = self.output.split()
		if "inside" in self.output:
			return(tcol.GREEN+cc[0]+tcol.RESET+"\t"+cc[1])
		elif "outside" in self.output:
			return(tcol.RED+cc[0]+tcol.RESET+"\t"+cc[1])

	def json(self):
		'''colors(): returns the result in JSON'''
		cc = self.output.split()
		status = ""
		if "inside" in cc[0]:
			status = "inside"
		elif "outside" in cc[0]:
			status = "outside"
		j = json.dumps({"scope":status, "host":cc[1]})
		return(j)

	def __repr__(self):
		'''__repr__(): returns the result'''
		self.check()
		return(self.output)
