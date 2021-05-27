#!/usr/bin/python3

# last updated: 2021-05-27
# usage:
#	test-scoper-examples.py -c test-burp-config.json

import argparse
import json
import sys
from scoper import ScoperSingle, ScoperList

parser = argparse.ArgumentParser(description="provide a Burp config and a file of URLs to check")
req = parser.add_argument_group("required arguments")
req.add_argument("-c", "--config", dest="config", type=str, help="path to a Burp configuration file", required=True)
args = vars(parser.parse_args())
configFile = args["config"]

########################################################

# note these are FAKE examples; provide ScoperSingle a string URL, or ScoperList a list of URLs
inputUrls = [
	"http://test.google.com/admin/stuff",
	"https://test.google.com/admin/stuff",
	"http://test.google.com",
	"https://test.google.com",
	"http://test.yahoo.com",
	"https://test.yahoo.com",
	"http://test.yahoo.com/administrator/stuff",
	"https://test.yahoo.com/administrator/stuff",
	"http://off-limits.google.com",
	"https://off-limits.google.com",
	"http://off-limits.yahoo.com",
	"https://off-limits.yahoo.com",
	"http://example.google.com",
	"https://example.google.com",
	"http://example.yahoo.com",
	"https://example.yahoo.com"
]

########################################################

print()
print("\\"*100)
print("load the config:", configFile)

with open(configFile, "r") as c:
	cnf = json.load(c)
c.close()

print("config contents:")
print(cnf)

print("/"*100)
print()

########################################################

print()
print("\\"*100)

print("ScoperSingle")
print()
for i in inputUrls:
	#s = ScoperSingle(config=configFile, url=i) # pass in a string path to the config file
	s = ScoperSingle(config=cnf, url=i) # pass in the config dict loaded above
	print(s.output)
	print(s.json)
	print(s.color)

print("/"*100)
print()

########################################################

print()
print("\\"*100)

print("ScoperList")
l = ScoperList(config=cnf, urls=inputUrls)
print()
print("dict output")
print(l.output) # different format than ScoperSingle
print()
print("JSON output")
print(l.json) # different format than ScoperSingle
print()
print("colorized string output")
print(l.color) # giant string containing newline characters
print("dict generator - similar output to ScoperSingle")
for i in l.output_generator():
	print(i)
print()
print("JSON generator - similar output to ScoperSingle")
for j in l.json_generator():
	print(j)

print("/"*100)
print()
