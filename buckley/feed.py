import reqhandlers 
from models import *

class Main(reqhandlers.Base):
  "Defines projects"
  def get(self, path):
    posts = Post.get_posts_published_cached(20)
    self.render_feed('feed2', {
      'posts': posts
    })