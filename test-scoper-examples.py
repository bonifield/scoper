#!/usr/bin/python3

# last updated: 2021-02-13
# usage:
#	test-scoper-examples.py -c test-burp-config.json

import argparse, json, sys
from scoper import ScoperList, ScoperSingle

parser = argparse.ArgumentParser(description="provide a Burp config and a file of URLs to check")
req = parser.add_argument_group("required arguments")
req.add_argument("-c", "--config", dest="config", type=str, help="path to a Burp configuration file", required=True)
args = vars(parser.parse_args())
configFile = args["config"]

with open(configFile, "r") as conf:
	c = json.load(conf)
conf.close()

# note these are FAKE examples; provide Scoper a single URL or list
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



print("\\"*100)
print("ScoperList returns ONLY included items after all checks have been made")
print("ScoperSingle returns BOTH included AND excluded items after all checks have been made")
print("/"*100)



print("\\"*100)
s = ScoperList(c, inputUrls)
#print(s.processIncludes.__doc__)
#print(s.processExcludes.__doc__)
#print(s.check.__doc__)
#print(s.gen.__doc__)
#print(s.colors.__doc__)
#print(s.__repr__.__doc__)
#print()
s.check()
print("MAIN OUTPUT LIST OBJECT: s.output")
print(s.output)
print("SECONDARY OUTPUT FROM __repr__")
print(s)
print("GENERATOR: gen()")
for x in s.gen():
	print(x)
print("GENERATOR WITH COLOR: colors()")
for x in s.colors():
	print(x)
print("JSON: json()")
for x in s.json():
	print(x)
print("/"*100)



print("\\"*100)
ss = ScoperSingle(c, "http://test.google.com/admin/stuff")
ss.check()
print(ss.output)
print(ss.colors())
print(ss.json())
print("/"*100)



print("\\"*100)
ss = ScoperSingle(c, "https://test.yahoo.com")
ss.check()
print(ss.output)
print(ss.colors())
print(ss.json())
print("/"*100)



print("\\"*100)
ss = ScoperSingle(c, "https://test.yahoo.com/administrator/stuff")
ss.check()
print(ss.output)
print(ss.colors())
print(ss.json())
print("/"*100)



print("\\"*100)
ss = ScoperSingle(c, "https://off-limits.yahoo.com")
ss.check()
print(ss.output)
print(ss.colors())
print(ss.json())
print("/"*100)



# use a loop over a list/generator/etc
print("\\"*100)
for i in inputUrls:
	sss = ScoperSingle(c, i)
	sss.check()
	print(sss.output)
	print(sss.colors())
	print(sss.json())
print("/"*100)
