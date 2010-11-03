# import buckley.Controller
import buckley
from buckley.models import *

class Index(buckley.Controller):
	def get(self, path):
		defaults = ['', '/', 'index', 'index.html', 'index.htm']
		if Post.stub_exists(path):
			posts = Post.get_single_by_stub(path)
			self.render('single', {
				'post': posts[0]
			})
		elif Post.is_key(path):
			posts = Post.get_single_by_key(path)
			self.render('single', {
				'post': posts
			})
		elif path in defaults:
			posts = Post.get_posts_published()
			self.render('index', {
				'posts': posts
			})
		else:
			self.render_error('File Not Found', 404)

def SinglePostHandler():
	def get(self, title):
		post = Post.stub_exists(title)
		if post:
			self.render('single', { 'post': post })
		else:
			self.render_error('File Not Found', 404)
