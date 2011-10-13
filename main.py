"""
A blogging tool
"""
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from vendor import *
from buckley import *

import buckley

routes = [
	('/feed(.*)', feed.Main),
	('/contact', buckley.pages.Contact),
	('/about', buckley.pages.About),
	('/archive(.*)', archive),
	('/admin/posts/(.*)/(.*)', admin.Posts),
	('/admin/posts/(.*)', admin.Posts),
	('/admin/posts', admin.Posts),
	('/admin/cache', admin.Cache),
	('/admin/cache_page/(.*)', admin.CacheView),
	('/admin/pages/(.*)/(.*)', admin.Pages),
	('/admin/pages/(.*)', admin.Pages),
	('/admin/pages', admin.Pages),
	('/admin/settings', admin.Settings),
	('/admin(.*)', admin.Settings),
	('/consulting(.*)', pages.Consulting),
	('/projects(.*)', projects.Main),
	('/soccer-gen', soccergen.SoccerGen),
	('/password-gen', projects.PasswordGen),
	('/tracking-cookie', projects.TrackingCookie),
	('/(.*)', blog)
]

plugins = {
	'most_recent': {
		'display_last': 10
		# 'css_class': 'sidebar_mr'
	},
	'disqus': {
		'site_id': 'nikcub'
	}
}

def main():
	app = Application(routes, plugins, debug=False)
	run_wsgi_app(app)

if __name__ == '__main__':
	main()
