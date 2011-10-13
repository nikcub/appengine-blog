import reqhandlers 
from models import *

class Main(reqhandlers.Base):
  "Defines projects"
  def get(self, path):
    posts, src = Post.get_posts_published_cached(10)
    self.render_feed('feed2', {
      'posts': posts,
      'src': src,
    })