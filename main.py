"""
A blogging tool
"""
import os, sys, logging, cgi, datetime, yaml, time, re

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from buckley import serialize
from vendor import *
from buckley import *
from pprint import pprint

def loginRequired(func):
  def wrapper(self, *args, **kw):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      func(self, *args, **kw)
  return wrapper

def timer(func):
	def wrapper(*arg):
		t1 = time.clock()
		res = func(*arg)
		t2 = time.clock()
		logging.info("%s took %0.3fms" % (func.func_name, (t2-t1) * 1000.0))
		return res
	return wrapper

def auth_decorator(func):
	return True

class BuckleyReqHandler(webapp.RequestHandler):
	def __init__(self):
		self.conf_load()
	
	def render(self, template_name, vars, response_type = ''):
		content = self.get_page(template_name, vars, response_type)
		self.response.clear()
		self.response.set_status(200)
		self.response.out.write(content)
	
	def get_page(self, template_name, vars, response_type = ''):
		if not response_type:
			response_type = self.get_response_type()
		
		vars = self.get_template_vars(vars)
		
		if response_type in ['xml']:
			self.response.headers['Content-Type'] = 'application/xml; charset=utf-8'
			content = serialize.atom(vars)
		elif response_type == 'json':
			self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
			content = serialize.json(vars)
		else:
			content = template.render(self.get_template(template_name, response_type), vars)
		
		return content
		
	def set_error(self, code, message):
		content = self.get_page('error', { 'message': message })
		self.response.clear()
		self.response.set_status(code)
		self.response.out.write(content)
		
	def get_template_vars(self, vars):
		# additional vars to send to temp
		additional = {
			'admin': self.is_admin(),
			'user': self.get_user(),
			'logout': users.create_logout_url('/'),
			'title': self.conf_get('title')
		}
		return dict(zip(vars.keys() + additional.keys(), vars.values() + additional.values()));
	
	def get_template(self, template_name, template_format = 'html'):
		return os.path.join(os.path.dirname(__file__), 'templates', template_name + '.' + template_format)
	
	def get_response_type(self):
		accept = self.request.headers['accept'].split(',')
		if accept[0] == 'application/json' or self.request.get('json'):
			return 'json'
		elif self.request.get('xml'):
			return 'xml'
		else:
			return 'html'
	
	def get_param_dict(self):
		params = {}
		for argument in self.request.arguments():
			params[argument] = self.request.get(argument)
		return params
	
	def get_uri_vars(self):
		# @todo make this not mental
		return self.request.path.strip('/').replace('///', '/').replace('//', '/').split('/')
	
	def slugify(self, value):
	    value = re.sub('[^\w\s-]', '', value).strip().lower()
	    return re.sub('[-\s]+', '-', value)
	
	def setconfig(value):
		self.config = value
	
	def user():
		user = users.get_current_user()
		if user:
			greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" % (user.nickname(), users.create_logout_url("/")))
			if users.is_current_user_admin():
				admin = "<a href=\"/admin/\">Go to admin area</a>"
		else:
		    greeting = ("<a href=\"%s\">Sign in or register</a>." %
		                users.create_login_url("/"))
		
		self.response.out.write("<html><body>%s<br />%s</body></html>" % (greeting, admin))
	
	def get_user(self):
		return users.get_current_user()
	
	def is_admin(self):
		user = users.get_current_user()
		return users.is_current_user_admin()
	
	def conf_get(self, var):
		return self.conf[var]
	
	def conf_load(self, refresh=False):
		val = memcache.get('blog.yaml')
		if val is None or refresh is True:
			file = open('blog.yaml', 'r')
			self.conf = yaml.load(file)
			memcache.add('blog.yaml', self.conf, 3600)
		else:
			self.conf = val;
	
	def get_stub(self, title, inc = 1):
		logging.info("Called with %s and %d" % (title, inc))
		stub_exists = Post.stub_exists(self.slugify(title))
		if stub_exists == False:
			return self.slugify(title)
		else:
			inc = inc + 1
			if inc > 2:
				return self.get_stub("%s-%d" % (self.slugify(title[:-2]), inc), inc)
			else:
				return self.get_stub("%s-%d" % (self.slugify(title), inc), inc)
	
	def is_post(self, id):
		if Post.is_key(id) or Post.is_slug(id):
			return True
		else:
			return False
	
	def handle_exception(self, two, three):
		logging.error(two)
		logging.error(three)

class blog(BuckleyReqHandler):
	"Defines the main blog"
	def get(self, path):
		defaults = ['', '/', 'index', 'index.html', 'index.htm']
		if Post.stub_exists(path):
			posts = Post.get_single_by_stub(path)
			self.render('single', {
				'post': posts,
				'path': path
			})
		elif Post.is_key(path):
			posts = Post.get_single_by_key(path)
			self.render('single', {
				'post': posts,
				'path': path
			})
		elif path in defaults:
			posts = Post.get_posts_published()
			self.render('index', {
				'posts': posts,
				'path': path
			})
		else:
			self.response.set_status(404)
			self.render('error', {
				'message': '404 - File Not Found'
			})

class admin(BuckleyReqHandler):
	def get(self, val):
		posts = Post.get_all()
		self.render('admin', {
			'posts': posts,
			'path': val
		})

class adminEdit(BuckleyReqHandler):
	def get(self, key):
		post = Post.get_single_by_key(key)
		self.render('edit', {
			'post': post
		})
	
	def post(self, key):
		post = Post.get_single_by_key(key)
		if not post:
			self.redirect('/error')
		z = post.update(self.get_param_dict())
		if z:
			self.redirect(self.request.url + '?success')
		else:
			self.redirect('/error')
		# r = post.update(self.request)
			# self.redirect('/error')
		# self.redirect(self.request.url + '?success')

class post(BuckleyReqHandler):
	def post(self):
		
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
		post.put()
		self.redirect('/admin')

class archive(BuckleyReqHandler):
	def get(self, when):
		if not when:
			when = 'all'
		# arch = 'month'
		# posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC LIMIT 10")
		posts = Post.get_last(100)
		self.render('archive', {
			'posts': posts
		})

class error(BuckleyReqHandler):
	def get(self):
		self.render('error', {
			'message': '404 - File Not Found'
		})

class dumpEnv(BuckleyReqHandler):
	def get(self):
		strVars = ""
		for name in os.environ.keys():
			strVars = strVars + "%s = %s<br />\n" % (name, os.environ[name])
		self.response.out.write("<html>" + strVars)

class SinglePostHandler(BuckleyReqHandler):
	def get(self, title):
		logging.info("Called SinglePostHandler with %s" % title)
		post = Post.stub_exists(title)
		if post:
			# posts = Post.get_single_by_stub(title)
			logging.info(post.title)
			self.render('single', {
				'post': post
			})
		else:
			self.set_error(404, 'File Not Found')
				
routes = [
	('/post', post),
	('/archive(.*)', archive),
	('/admin/edit/(.*)', adminEdit),
	('/admin(.*)', admin),
	('/error', error),
	('/(.*)\.html', SinglePostHandler),
	('/env', dumpEnv),
	('/(.*)', blog)
]

def main():
	app = webapp.WSGIApplication(routes, debug=True)
	run_wsgi_app(app)

if __name__ == '__main__':
	main()
