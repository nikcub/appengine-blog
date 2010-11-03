import buckley
from buckley.models import *

class Projects(buckley.Controller):
	"Defines projects"
	def get(self, path):
		self.render('projects', {})
