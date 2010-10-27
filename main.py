"""
A blogging tool
"""
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from vendor import *
from buckley import *

routes = [
	('/feed(.*)', feed.Main),
	('/archive(.*)', archive),
	('/admin/posts/(.*)/(.*)', admin.Posts),
	('/admin/posts/(.*)', admin.Posts),
	('/admin/posts', admin.Posts),
	('/admin/pages/(.*)/(.*)', admin.Pages),
	('/admin/pages/(.*)', admin.Pages),
	('/admin/pages', admin.Pages),
	('/admin/settings', admin.Settings),
	('/admin(.*)', admin.Settings),
	('/projects(.*)', projects.Main),
	('/(.*)\.html', SinglePostHandler),
	('/(.*)', blog)
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
