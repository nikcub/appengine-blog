import buckley
from buckley.models import *

class Feeds(buckley.Controller):
	"Defines projects"
	def get(self, path):
		posts = Post.get_last(10)
		self.render_feed('feed2', {
			'posts': posts
		})