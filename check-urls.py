#!/usr/bin/python3

# example usage:
#	check-url.py -c test-burp-config.conf -u test-urls.json -m [single|list]

import argparse, json, sys
from scoper import ScoperList, ScoperSingle

parser = argparse.ArgumentParser(description="provide a Burp config and a file of URLs to check")
req = parser.add_argument_group("required arguments")
req.add_argument("-c", "--config", dest="config", type=str, help="path to a Burp configuration file", required=True)
req.add_argument("-u", "--urlfile", dest="url", type=str, help="path to a file containing URLs to check", required=True)
req.add_argument("-p", "--process", dest="mode", type=str, help="processing mode: [single|list]", required=True)
args = vars(parser.parse_args())
configFile = args["config"]
urlFile = args["url"]
process = args["process"]

with open(configFile, "r") as conf:
        c = json.load(conf)
conf.close()

if process == "single":
	# CHECK USING SINGLE, READS ONE LINE OF URL FILE AT A TIME
	with open(urlFile, "r") as f:
		counter = 0
		for line in f:
			counter += 1
			l = json.loads(line)
			h = l["host"]
			if "http" not in h:
				for x in ["http://", "https://"]:
					s = ScoperSingle(c, x+h)
					s.check()
					print(s.json())
#					print(s.output)
#					print(s.colors())
			else:
				s = ScoperSingle(c, h)
				s.check()
				print(s.colors())
#				print(s.output())
#				print(s.colors())
		#sys.stderr.write("parsed "+str(counter)+" items\n")
	f.close()
elif process == "list":
	# CHECK USING LIST, READS ENTIRE URL FILE INTO MEMORY
	with open(urlFile, "r") as f:
		counter = 0
		u = []
		for line in f:
			counter += 1
			l = json.loads(line)
			h = l["host"]
			if "http" not in h:
				for x in ["http://", "https://"]:
					u.append(x+h)
			else:
				u.append(h)
		s = ScoperList(c, u)
		s.check()
		for j in s.json():
			print(j)
	#	for o in s.output():
	#		print(o)
	#	for c in s.colors():
	#		print(c)
		#sys.stderr.write("parsed "+str(counter)+" items\n")
	f.close()
else:
	print('specify "-p single" or "-p list"')
	sys.exit(1)
