from buckley.plugin import *
from buckley.models import *
import logging

class most_recent(Plugin_base):
	
	
	def initialize(self, one):
		# logging.info("Initialized most_recent %s %s" % (self, one))
		template = self.get_template()
		return True
		
	def render(self):
		ret = {}
		posts = Post.get_last(5)
		if self.get_conf('css_class'):
			css_class = self.get_conf('css_class')
		else:
			css_class = "most_recent"
		
		return {'most_recent': self.render_template({
			'posts': posts,
			'css_class': css_class
		})}
		
	# def get_most_recent(self, num = 5):

		
	