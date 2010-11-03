import buckley
from buckley.models import *

class Pages(buckley.Controller):
	def get(self, path):
		self.render('Not Implemented', 404)