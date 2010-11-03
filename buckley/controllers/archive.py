import buckley
from buckley.models import *

class Archives(buckley.Controller):
	def get(self, when):
		if not when:
			when = 'all'
		# arch = 'month'
		# posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC LIMIT 10")
		posts = Post.get_posts_published(100)
		self.render('archive', {
			'posts': posts
		})
