import sys, datetime, logging
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from buckley.datatypes import *

class Asset(db.Model):
	# key = stub
	parent = db.ReferenceProperty(Asset)
	author = db.UserProperty()
	title = db.StringProperty(required=True)
	excerpt = db.StringProperty(multiline=True)
	content = db.TextProperty()
	content_html = HtmlFromMarkdownProperty(source = content, default = None)
	asset_type = db.StringProperty(choices = set(['post', 'page']))
	status = db.StringProperty(required = True, choices = set(['draft', 'scheduled', 'published']))
	categories = db.ListProperty(db.Category)
	stub = db.StringProperty()
	permalink = db.StringProperty()
	pubdate = db.DateTimeProperty()
	draftdate = db.DateTimeProperty(auto_now_add=True)

	
	
	
	