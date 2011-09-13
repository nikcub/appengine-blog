
# todo inherit from built in user property support twitter et al

class User(db.Model):
	name = db.StringProperty()
	email = db.StringProperty()
	author = db.UserProperty()