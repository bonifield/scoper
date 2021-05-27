# scoper
test a single URL, or a list of URLs, against a Burp Suite-style JSON configuration file to determine in/out-of-scope status

## installation ([GitHub](https://github.com/bonifield/scoper) / [PyPi](https://pypi.org/project/scoper/))
```
pip install scoper
```

## importing and loading the external Burp-style configuration file
- imports and loading the configuration file in your script
```
import json
from scoper import ScoperList, ScoperSingle
with open("test-burp-config.json", "r") as conf:
	c = json.load(conf)
conf.close()
```

## ScoperSingle
- check a single URL (provide a string)
```
#s = ScoperSingle(config="/path/to/config.json", url="http://test.google.com/admin/stuff") # pass in a string path to the config file
s = ScoperSingle(config=c, url="http://test.google.com/admin/stuff") # note "c" is the config loaded above
print(s.output) # single dict
print(s.json) # single JSON string
print(s.color) # single colorized string
# if passing in a dict for the config, loop over a list of URLs etc while only opening the config once
```
- loop over multiple URLs "inputUrls" and process them one at a time
```
for i in inputUrls:
	#sss = ScoperSingle(config="/path/to/config.json", url="http://test.google.com/admin/stuff") # pass in a string path to the config file
	sss = ScoperSingle(config=c, url="http://test.google.com/admin/stuff") # note "c" is the config loaded above
	print(sss.output) # single dict
	print(sss.json) # single JSON string
	print(sss.colors) # single colorized string
```

## ScoperList
- bulk-process multiple URLs (provide a list)
```
l = ScoperList(config=c, urls=inputUrls) # note "c" is the config loaded above, inputUrls is a list object
# dict object, NOT the same format as ScoperSingle
print(l.output)
# JSON object, NOT the same format as ScoperSingle
print(l.json)
# generator, dict output in the SAME format as ScoperSingle
for x in l.output_generator():
	print(x)
# generator, JSON output in the SAME format as ScoperSingle
for x in l.json_generator():
	print(x)
# large colorized string with newline characters for on-screen viewing
print(l.color)
```

## example output
![example scoper output](https://github.com/bonifield/scoper/raw/main/images/example-scoper-output.PNG)

### Release Notes
- v1.1.0
	- major overhaul to streamline code
	- made output functions in ScoperList into generators
	- fixed some logic that determines inside/outside of scope
- v1.0.21
	- simplified import structure
	- minor typo fixes
