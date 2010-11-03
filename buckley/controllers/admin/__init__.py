import buckley
from buckley.models import *
from pages import *
from posts import *
from settings import *

class Admin(buckley.Controller):
	def initialize(self, request, response):
		self.request = request
		self.response = response
		user = users.get_current_user()
		if not user or not users.is_current_user_admin():
			raise AppAuthError

	def is_admin():
		return users

	def get_template_path(self, template_name, template_format = 'html'):
		return os.path.join(os.path.dirname(__file__), 'templates', template_name + '.' + template_format)
