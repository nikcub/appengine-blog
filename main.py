"""
A blogging tool
"""
from google.appengine.ext.webapp.util import run_wsgi_app
from vendor import *
from buckley import *


routes = [

	# ('/admin/posts/(.*)/(.*)', controllers.admin.Posts),
	# ('/admin/posts/(.*)', controllers.admin.Posts),
	# ('/admin/posts', controllers.admin.Posts),
	# ('/admin/pages/(.*)/(.*)', controllers.admin.Pages),
	# ('/admin/pages/(.*)', controllers.admin.Pages),
	# ('/admin/pages', controllers.admin.Pages),
	# ('/admin/settings', controllers.admin.Settings),
	# ('/admin(.*)', controllers.admin.Settings),
	# 
	# ('/feed(.*)', controllers.Feeds),
	# ('/archive(.*)', controllers.Archives),
	# ('/projects(.*)', controllers.Projects),
	# ('/posts(.*)', controllers.posts.Index),
	('/(.*)', controllers.posts.Index)
]

plugins = {
	'most_recent': {
		'display_last': 5
		# 'css_class': 'sidebar_mr'
	},
	'disqus': {
		'site_id': 'nikcub'
	}
}

def main():
	app = Application(routes, plugins, debug=True)
	run_wsgi_app(app)

if __name__ == '__main__':
	main()
