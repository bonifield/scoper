#!/usr/bin/python3

# last updated: 2021-05-27

# example usage:
#	check-url.py -c burp-config.conf -u urls.json -f url -m [single|list]

import argparse
import json
import sys
from scoper import ScoperList, ScoperSingle

parser = argparse.ArgumentParser(description="provide a Burp config and a file of URLs to check")
req = parser.add_argument_group("required arguments")
req.add_argument("-c", "--config", dest="config", type=str, help="path to a Burp configuration file", required=True)
req.add_argument("-u", "--urlfile", dest="url", type=str, help="path to a file containing URLs to check", required=True)
req.add_argument("-f", "--field", dest="field", type=str, help="field name in JSON to check", required=True)
req.add_argument("-m", "--mode", dest="mode", type=str, help="mode: [single|list]", required=True)
args = vars(parser.parse_args())
configFile = args["config"]
urlFile = args["url"]
mode = args["mode"]
fieldName = args["field"]

with open(configFile, "r") as conf:
        c = json.load(conf)
conf.close()

if mode == "single":
	# CHECK USING SINGLE, READS ONE LINE OF URL FILE AT A TIME
	with open(urlFile, "r") as f:
		counter = 0
		for line in f:
			counter += 1
			l = json.loads(line)
			#h = l["host"]
			#h = l["url"]
			h = l[fieldName]
			if "http" not in h:
				for x in ["http://", "https://"]:
					s = ScoperSingle(config=c, url=x+h)
					print(s.json)
			else:
				s = ScoperSingle(config=c, url=h)
				print(s.json)
		#sys.stderr.write("parsed "+str(counter)+" items\n")
	f.close()
elif mode == "list":
	# CHECK USING LIST, READS ENTIRE URL FILE INTO MEMORY
	with open(urlFile, "r") as f:
		counter = 0
		u = []
		for line in f:
			counter += 1
			l = json.loads(line)
			#h = l["host"]
			#h = l["url"]
			h = l[fieldName]
			if "http" not in h:
				for x in ["http://", "https://"]:
					u.append(x+h)
			else:
				u.append(h)
		s = ScoperList(config=c, urls=u)
		for j in s.json_generator():
			print(j)
		#sys.stderr.write("parsed "+str(counter)+" items\n")
	f.close()
else:
	print('specify "-m single" or "-m list"')
	sys.exit(1)
