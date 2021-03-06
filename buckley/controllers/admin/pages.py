import buckley
from buckley.models import *

class Pages(buckley.controllers.Admin):
	def get(self, action=False, key=False):
		if action == 'edit' and key:
			posts = Post.get_single_by_key(key)
			self.render('pages.edit', {
				'post': posts,
				'post_type': 'page'
			})
		else:
			posts = Post.get_all_pages()
			self.render('pages', {
				'posts': posts,
				'post_type': 'page'
			})
		
	def post(self, action = False, key = False):
		if action == 'edit' and key:
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
		else:
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
				author = users.get_current_user(),
				post_type = 'page',
				stub = self.slugify(title),
				pubdate = datetime.datetime.now()
			)
			r = post.put()
			self.redirect('/admin/pages/edit/' + str(r))