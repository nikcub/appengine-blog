import sys
import datetime
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from buckley.datatypes import HtmlFromMarkdownProperty, StubFromTitleProperty

class Post(db.Model):
  author = db.UserProperty()
  title = db.StringProperty(required=True)
  excerpt = db.StringProperty(multiline=True)
  content = db.TextProperty()
  content_html = HtmlFromMarkdownProperty(source = content, default = None)
  post_type = db.StringProperty(choices = set(['post', 'page']))
  status = db.StringProperty(required = True, choices = set(['draft', 'scheduled', 'published']))
  categories = db.ListProperty(db.Category)
  new_stub = StubFromTitleProperty(source = title, default = None)
  stub = db.StringProperty()
  permalink = db.StringProperty()
  
  featured = db.BooleanProperty()
  pubdate = db.DateTimeProperty(auto_now_add=True)
  
  def create_new(title, content, categories = []):
    
    cats = []
    for category in categories:
      cats.append(db.Category(category))
      
    post = Post(
      title = title,
      excerpt = content[:250],
      content = content, 
      status = "draft",
      categories = cats,
      stub = self.get_stub(title),
      author = users.get_current_user(), 
      post_type = "post",
      pubdate = datetime.datetime.now()
    )
    
    try:
      post.put()
    except CapabilityDisabledError:
      return false
    return true 
  
  def update(self, values):
    for arg in values:
      if hasattr(self, arg) and values[arg] != getattr(self, arg):
        setattr(self, arg, values[arg])
    try:
      z = self.put()
      return True
    except CapabilityDisabledError:
      logging.error('yep')
  
  @classmethod
  def get_posts_published(self, num = 5):
    # query = db.Query(Post).filter('post_type = 'post'').order('-pubdate')
    query = db.GqlQuery("select * from Post where post_type='post' and status='published' order by pubdate DESC")
    return query.fetch(num)

  @classmethod
  def get_posts_published_cached(self, num=10, cache=False, key='index'):
    dat_key = "%s.%s" % ('models', key)
    dat = memcache.get(dat_key)
    if dat is not None and cache == False:
      return dat, 'memcache'
    else:
      query = db.GqlQuery("select * from Post where post_type='post' and status='published' order by pubdate DESC")
      r = memcache.set(dat_key, query.fetch(num))
      if not r:
        logging.error("Memcache: Could not set cache for %s" % dat_key)
      else:
        logging.info("Memcache: Set post key as %s" % dat_key)
    return query.fetch(num), 'database'

  def publish(self):
    self.status = 'published'
    self.put()

  @classmethod
  def get_all(self, num = 5):
    # query = db.Query(Post).filter('post_type = 'post').order('-pubdate')
    query = self.all().filter('post_type =', 'post').order('-pubdate')
    return query.fetch(num)

  @classmethod
  def get_all_pages(self, num = 5):
    query = db.Query(Post).filter('post_type =', 'page').order('-pubdate')
    # query = self.all().filter('post_type =', 'pages').order('-pubdate')
    return query.fetch(num)
            
  @classmethod
  def get_last(self, num = 5):
    # query = db.Query(Post).filter('post_type = 'post'').order('-pubdate')
    # query = self.all().filter('post_type = ', 'post').filter('status = ', 'published').order('-pubdate')
    query = db.GqlQuery("select * from Post where post_type='post' and status='published' order by pubdate DESC")
    # query.filter('limit 5')
    # query.order('-pubdate')
    return query.fetch(num)

  @classmethod
  def get_month(month, year):
    if not month:
      month = datetime.datetime.now().month
    if not year:
      year = datetime.datetime.now().year
  
  @classmethod
  def page_cache(self, stub):
    pass

  @classmethod
  def stub_exists(self, stub = '', cache=False):
    dat_key = "%s.%s" % ('models', stub)
    dat = memcache.get(dat_key)
    if dat is not None and not cache:
      return dat, 'memcache'
    else:    
      query = db.GqlQuery("select * from Post where stub = :1", stub)
      if query.count() == 0:
        return None, None
      rec = query.fetch(1)
      if rec[0].status == 'published':
        r = memcache.set(dat_key, rec)
        if not r:
          logging.error("Memcache: Could not set cache for %s" % dat_key)
        else:
          logging.info("Memcache: Set post key as %s" % dat_key)
      return rec, 'database'
  
  @classmethod
  def is_key(self, k):
    try:
      query = db.get(db.Key(k))
    except:
      return False
    return True
  
  @classmethod
  def is_slug(self, key):
    return self.stub_exists(key)
  
  @classmethod
  def get_single_by_key(self, key):
    return db.get(db.Key(key))

  @classmethod
  def get_single_by_stub(self, stub):
    dat_key = "%s.%s" % ('models', stub)
    dat = memcache.get(dat_key)
    if dat is not None:
      logging.info(dat)
      return dat
    else:
      query = db.GqlQuery("select * from Post where stub = :1", stub)
      r = memcache.set(dat_key, query.fetch(1))
      if not r:
        logging.error("Memcache: Could not set cache for %s" % dat_key)
      else:
        logging.info("Memcache: Set post key as %s" % dat_key)
    return query.fetch(1)

  @classmethod
  def to_dict(self):
    return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

