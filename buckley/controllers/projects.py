import reqhandlers 
from models import *

class Main(reqhandlers.Base):
	"Defines projects"
	def get(self, path):
		self.render('projects', {})
