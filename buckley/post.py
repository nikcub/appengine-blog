import reqhandlers 
from models import *

class about(reqhandlers.Base):
  def get(self):
    return self.render('about', {'tab_about': True})

class blog(reqhandlers.Base):
	"Defines the main blog"
	def get(self, path):
		defaults = ['', '/', 'index', 'index.html', 'index.htm']
		if Post.stub_exists(path):
			posts = Post.get_single_by_stub(path)
			self.render('single', {
				'post': posts[0],
				'tab_blog': True
			})
		elif Post.is_key(path):
			posts = Post.get_single_by_key(path)
			self.render('single', {
				'post': posts,
				'tab_blog': True
			})
		elif path in defaults:
			posts = Post.get_posts_published()
			self.render('index', {
				'posts': posts,
				'tab_blog': True
			})
		else:
			self.render_error('File Not Found', 404)

class SinglePostHandler(reqhandlers.Base):
	def get(self, title):
		post = Post.stub_exists(title)
		if post:
			self.render('single', { 'post': post,
				'tab_blog': True })
		else:
			self.render_error('File Not Found', 404)
