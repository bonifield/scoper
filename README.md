# scoper
test a single URL, or a list of URLs, against a Burp Suite-style JSON configuration file to determine scope

## examples
- example script
```
test-scoper-examples.py -c test-burp-config.json
```
- imports and loading the configuration file in your script
```
import json, sys
from scoper import ScoperList, ScoperSingle
with open(sys.argv[1], "r") as conf:
	c = json.load(conf)
conf.close()
```
- provide a Python list "inputUrls" consisting of URLs, and only retrieve "INSIDE-SCOPE"
```
s = ScoperList(c, inputUrls)
s.check()
print(s.output)
# generator, plain strings
for x in s.gen():
	print(x)
# generator, colorized strings for on-screen viewing
for x in s.colors():
	print(x)
```
- check a single URL for "INSIDE-SCOPE" or "OUTSIDE-SCOPE" status
```
ss = ScoperSingle(c, "http://test.google.com/admin/stuff")
ss.check()
print(ss.output)
print(ss.colors())
```
- loop over a Python list "inputUrls" and process them one at a time for either INSIDE-SCOPE or OUTSIDE-SCOPE status
```
for i in inputUrls:
	sss = ScoperSingle(c, i)
	sss.check()
	print(sss.output)
	print(sss.colors())
```
