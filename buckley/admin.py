import reqhandlers 
from models import *

class Settings(reqhandlers.Admin):
	def get(self, val):
		settings = self.conf
		self.render('settings', {
			'settings': settings
		})
	def post(self):
		self.render_error('not yet implemented')


class Posts(reqhandlers.Admin):
	def get(self, val):
		posts = Post.get_all()
		self.render('posts', {
			'posts': posts
		})
		
	def post(self, key):

		title = self.request.get('title')
		content = self.request.get('content')
		categories = [db.Category('none')]
		excerpt = content[:250]

		post = Post(
			title = title,
			excerpt = excerpt,
			content = content,
			status = "draft",
			categories = categories,
			stub = self.get_stub(title),
			author = users.get_current_user(),
			post_type = "post",
			pubdate = datetime.datetime.now()
		)
		r = post.put()
		self.redirect('/admin/posts/edit/' + str(r))

class Pages(reqhandlers.Admin):
	def get(self, val):
		posts = Post.get_all_pages()
		self.render('posts', {
			'posts': posts
		})
	
	def post(self, key):
		return


class adminEdit(reqhandlers.Admin):
	def get(self, key):
		post = Post.get_single_by_key(key)
		self.render('posts.edit', {
			'post': post
		})
	
	def post(self, key):
		post = Post.get_single_by_key(key)
		if not post:
			self.redirect('/error')
		z = post.update(self.get_param_dict())
		if self.request.get('action') == 'publish':
			post.publish()
		if z:
			self.redirect(self.request.url + '?success')
		else:
			self.redirect('/error')
		# r = post.update(self.request)
			# self.redirect('/error')
		# self.redirect(self.request.url + '?success')
