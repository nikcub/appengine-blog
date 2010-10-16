from google.appengine.ext import db

class User(db.Model):
	name = db.StringProperty()
	email = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)

class Post(db.Model):
	title = db.StringProperty()
	content = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)