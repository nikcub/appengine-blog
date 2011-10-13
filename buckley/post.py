import reqhandlers 
import logging
from google.appengine.api import memcache
from models import *

class about(reqhandlers.Base):
  def get(self):
    return self.render('about', {'tab_about': True})

class blog(reqhandlers.Base):
  "Defines the main blog"
  def get(self, path):
    defaults = ['', '/', 'index', 'index.html', 'index.htm']
    host = self.request.environ['HTTP_HOST']
    cached_pages = ['logging-out-of-facebook-is-not-enough']
    referred_cache = self.request.get('ref', False)
    
    # if path in cached_pages:
      # return self.redirect("http://nikcub-static02.appspot.com/" + path)
    if path == 'facebook-fixes-logout-issue':
      return self.redirect('http://' + host + '/' + 'facebook-fixes-logout-issue-explains-cookies', permanent=True)

    if host not in ['localhost:9090', 'nikcub.appspot.com'] and not referred_cache:
      return self.redirect("http://nikcub.appspot.com/" + path, permanent = True)

    cache = self.request.get('cache', False)
    
    if not cache:
      page_cache = memcache.get('post.%s' % path)
      if page_cache:
        return self.render_content(page_cache)
    
    p, src = Post.stub_exists(path, cache)
    if p:
      # posts = Post.get_single_by_stub(path)
      # logging.info('get_single_by_stub')
      self.render('single', {
        'post': p[0],
        'tab_blog': True,
        'src': src,
      })
    elif path in defaults:
      posts, src = Post.get_posts_published_cached(5, cache)
      self.render('index', {
        'posts': posts,
        'tab_blog': True,
        'src': src,
      })
    elif Post.is_key(path):
      posts = Post.get_single_by_key(path)
      self.render('single', {
        'post': posts,
        'tab_blog': True
      })
    else:
      self.render_error('File Not Found', 404)

class SinglePostHandler(reqhandlers.Base):
  def get(self, title):
    post = Post.stub_exists(title)
    if post:
      self.render('single', { 'post': post,
        'tab_blog': True })
    else:
      self.render_error('File Not Found', 404)
