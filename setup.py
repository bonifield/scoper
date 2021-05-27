from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
	name='scoper',
	version='1.1.0',
	author='James Bonifield',
	author_email='bonifield.tools@gmail.com',
	description='test a single URL, or a list of URLs, against a Burp Suite-style JSON configuration file to determine in/out-of-scope status',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/bonifield/scoper/',
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	py_modules=["scoper"]
)