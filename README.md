# scoper
test a single URL, or a list of URLs, against a Burp Suite-style JSON configuration file to determine scope

## example output
![scoper-output-colorized.png](https://github.com/bonifield/scoper/raw/main/scoper-output-colorized.PNG)

## usage
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
- ScoperList: bulk-process a provided Python list "inputUrls" consisting of URLs, which only retrieves "INSIDE-SCOPE"
```
s = ScoperList(c, inputUrls) # note "c" is the config loaded above
s.check()
print(s.output) # list object
# generator, plain strings
for x in s.gen():
	print(x)
# generator, colorized strings for on-screen viewing
for x in s.colors():
	print(x)
```
- ScoperSingle: check a single URL for "INSIDE-SCOPE" or "OUTSIDE-SCOPE" status
```
ss = ScoperSingle(c, "http://test.google.com/admin/stuff") # note "c" is the config loaded above
ss.check()
print(ss.output) # single plaintext string
print(ss.colors()) # single colorized string
```
- ScoperSingle: loop over a Python list "inputUrls" and process them one at a time for either INSIDE-SCOPE or OUTSIDE-SCOPE status
```
for i in inputUrls:
	sss = ScoperSingle(c, i) # note "c" is the config loaded above
	sss.check()
	print(sss.output) # single plaintext string
	print(sss.colors()) # single colorized string
```
