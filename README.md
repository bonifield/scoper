# scoper
test a single URL, or a list of URLs, against a Burp Suite-style JSON configuration file to determine in/out-of-scope status

## installation
```
pip3 install scoper
```

## example output
- colorized terminal output\
![scoper-output-colorized.png](https://github.com/bonifield/scoper/raw/main/images/scoper-output-colorized.PNG)
- JSON output\
![scoper-output-json.png](https://github.com/bonifield/scoper/raw/main/images/scoper-output-json.PNG)

## importing and loading the external Burp-style configuration file
- imports and loading the configuration file in your script
```
import json, sys
from scoper.scoper import ScoperList
from scoper.scoper import ScoperSingle
with open(sys.argv[1], "r") as conf:
	c = json.load(conf)
conf.close()
```
- ScoperList: bulk-process a provided Python **list structure "inputUrls" consisting of URLs**, which only retrieves "inside-scope"
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
# generator, JSON strings for on-screen viewing
for x in s.json():
	print(x)
```
- ScoperSingle: check a **single URL string** for "inside-scope" or "ouside-scope" status
```
ss = ScoperSingle(c, "http://test.google.com/admin/stuff") # note "c" is the config loaded above
ss.check()
print(ss.output) # single plaintext string
print(ss.colors()) # single colorized string
print(ss.json()) # single JSON string
```
- ScoperSingle: loop over a Python **list structure "inputUrls" consisting of URLs** and process them one at a time for either "inside-scope" or "ouside-scope" status
```
for i in inputUrls:
	sss = ScoperSingle(c, i) # note "c" is the config loaded above
	sss.check()
	print(sss.output) # single plaintext string
	print(sss.colors()) # single colorized string
	print(ss.json()) # single JSON string
```

## sample scripts
- check-urls.py - quickly parse an input file containing JSON lines (from Amass, Subfinder, custom tooling, etc) against a Burp-style configuration file
```
check-urls.py -c test-burp-config.conf -u test-urls.json -p [single|list]
```
- use the example script to preview output formats
```
test-scoper-examples.py -c test-burp-config.json
```
