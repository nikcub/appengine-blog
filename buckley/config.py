from vendor import yaml
from google.appengine.api import memcache

class config(dict):
	def __init__(self, file):
		self.load(file)
		
	def load(self, file, refresh=False):
		val = memcache.get('blog.yaml')
		if val is None or refresh is True:
			file_contents = open(file, 'r')
			conf_parsed = yaml.load(file_contents)
			memcache.add('blog.yaml', conf_parsed, 60)
		else:
			conf_parsed = val;
		dict.__init__(self, conf_parsed)
