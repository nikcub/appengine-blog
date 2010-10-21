import reqhandlers 
from models import *

class archive(reqhandlers.Base):
	def get(self, when):
		if not when:
			when = 'all'
		# arch = 'month'
		# posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC LIMIT 10")
		posts = Post.get_last(100)
		self.render('archive', {
			'posts': posts
		})
