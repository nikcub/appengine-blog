from buckley.plugin import *
import logging

# this isn't done. i couldn't get disqus to work. oh well
class disqus(Plugin_base):
	
	identifier = ''
	url = ''
	enabled = True
	
	def initialize(self, test):
		return True
	
	def render(self):
		return {"disqus": "rende Disqus"}