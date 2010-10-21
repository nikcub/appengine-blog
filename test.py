#!/usr/bin/python

import yaml

class config(dict):
	def __init__(self, file):
		self.load(file)
		
	def load(self, file):
		self.file = open(file, 'r')
		self.conf = yaml.load(self.file)
		dict.__init__(self, self.conf)
		
conf = config('blog.yaml')
# print conf.conf

if conf.has_key('title'):
	print conf['title']