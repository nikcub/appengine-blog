
class Comment(db.Model):
	name = db.StringProperty()
	email = db.StringProperty()
	content = db.TextProperty()
	pubdate = db.DateTimeProperty(auto_now_add=True)
	views = db.IntegerProperty(default=0)
	
	def get_views(self):
		viewcount = self.views
		viewcount_cache = memcache.get('test-views-' + self.key().name(), self.key().kind())
		if viewcount_cache:
			viewcount += viewcount_cache
		return viewcount
		
	@classmethod
	def flush_views(cls, name):
		te