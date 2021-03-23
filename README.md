# scoper
test a single URL, or a list of URLs, against a Burp Suite-style JSON configuration file to determine in/out-of-scope status

## installation
```
pip install scoper
```

## example outputs
- terminal with colors
![scoper-output-colorized.PNG](https://github.com/bonifield/scoper/raw/main/images/scoper-output-colorized.PNG)
- JSON
![scoper-output-json.PNG](https://github.com/bonifield/scoper/raw/main/images/scoper-output-json.PNG)

## importing and loading the external Burp-style configuration file
- imports and loading the configuration file in your script
```
import json
from scoper import ScoperList, ScoperSingle
with open("test-burp-config.json", "r") as conf:
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
	print(sss.json()) # single JSON string
```

### Release Notes
- v1.0.21
	- simplified import structure
	- minor typo fixes
