import time
from google.appengine.api import users

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
