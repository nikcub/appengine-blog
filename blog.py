import os, logging
from google.appengine.ext import db
from models import *
from vendor import markdown
import web

urls = (
	'/post', 'post',
	'/archive(.*)', 'archive',
	'/admin', 'admin',
	'/error', 'error',
	'/(.*)', 'blog'
)

render = web.template.render('templates', base='base')

logging.info('Started')

class blog:
	def GET(self, path):
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC LIMIT 10")
		return render.index(posts, path)
		# posts = Post.gql("where author = :1 order by date desc", user.id)
		
class post:
	def GET(self):
		return ''
	def POST(self):
		post = Post()
		t = web.input('title')
		c = web.input('content')
		
		content = markdown.markdown(c.content)
		post.title = t.title
		post.content = content
		post.put()
		# return (t.title + ' ---- ' + c.content)
		return web.seeother('/admin')

class archive:
	def GET(self, when):
		# arch = 'month'
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC LIMIT 10")
		return render.archive(posts, when)
	
class admin:
	def GET(self):
		posts = db.GqlQuery("select * from Post order by date desc")
		return render.admin(posts)

class error:
	def GET(self):
		message = '404 - File Not Found'
		return                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
		
app = web.application(urls, globals())
main = app.cgirun()