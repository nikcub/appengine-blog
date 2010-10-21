"""
A blogging tool
"""
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from vendor import *
from buckley import *

routes = [
	('/archive(.*)', archive),
	('/admin/posts(.*)', admin.Posts),
	('/admin/pages(.*)', admin.Pages),
	('/admin/settings', admin.Settings),
	('/admin(.*)', admin.Settings),
	('/(.*)\.html', SinglePostHandler),
	('/(.*)', blog)
]

def main():
	app = Application(routes, debug=True)
	# try:
	run_wsgi_app(app)
	# except AdminAuthError:
		# print 'oh oh'

if __name__ == '__main__':
	main()
