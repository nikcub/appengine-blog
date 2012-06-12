import logging
import reqhandlers 
from models import *

class PasswordGen(reqhandlers.Base):
  def get(self):
    self.render('password-gen', {})
    
class TrackingCookie(reqhandlers.Base):
  def get(self):
    import uuid
    meth = self.request.get("_action", None)
    uid = uuid.uuid1()
    msg = ""

    # logging.info(self.request.headers)
    # logging.info(self.request.environ)
    # logging.info(self.response.headers)
    
    if 'If-Match' in self.request.headers:
      etag = self.request.headers['If-Match']
    else:
      etag = False

    if 'If-Modified-Since' in self.request.headers:
      lm = self.request.headers['If-Modified-Since']
    else:
      lm = False
    
    if meth == "etag" or not etag:
      self.response.headers['ETag'] = uid
      msg = "Set Etag header"
    
    if meth == "lm":
      self.response.headers['Last-Modified'] = uid
      msg = "Set Last-Modified header"

    del self.response.headers['Expires']
    
    self.render('tracking-cookie', {
      'msg': msg,
      'etag': etag,
      'lm': lm,
      'req': self.request.headers,
      'res': self.response.headers,
      'tab_projects': True
    })
    
  def post(self):

    if 'If-Match' in self.request.headers:
      etag = self.request.headers['If-Match']
    else:
      etag = False

    if 'If-Modified-Since' in self.request.headers:
      lm = self.request.headers['If-Modified-Since']
    else:
      lm = False
    
    logging.info('if_match:')
    logging.info(self.request.if_match)
    logging.info('if_modified:')
    logging.info(self.request.if_modified_since)
    
    if not etag:
      self.response.headers['ETag'] = uid
    
    if not lm:
      self.response.headers['Last-Modified'] = uid
    
    return self.redirect('/tracking-cookie?s')
    self.render('tracking-cookie', {
      'action': meth,
      'etag': etag,
      'lm': lm,
    })