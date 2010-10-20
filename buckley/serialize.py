import datetime  
import time 
import logging

from google.appengine.api import users 
from google.appengine.ext import db 

#this is a mod on the orinal file for some reason it includes its own simplejson files i have ref django!
from django.utils import simplejson  

class GqlEncoder(simplejson.JSONEncoder): 
  """Extends JSONEncoder to add support for GQL results and properties. 

  Adds support to simplejson JSONEncoders for GQL results and properties by 
  overriding JSONEncoder's default method. 
  """ 
  # TODO Improve coverage for all of App Engine's Property types. 
  def default(self, obj): 
    """Tests the input object, obj, to encode as JSON.""" 

    if hasattr(obj, '__json__'): 
      return getattr(obj, '__json__')() 

    if isinstance(obj, db.GqlQuery): 
      return list(obj) 

    elif isinstance(obj, db.Model): 
      properties = obj.properties().items() 
      output = {} 
      for field, value in properties: 
        output[field] = getattr(obj, field) 
      return output 

    elif isinstance(obj, datetime.datetime): 
      output = {} 
      fields = ['day', 'hour', 'microsecond', 'minute', 'month', 'second', 
          'year'] 
      methods = ['ctime', 'isocalendar', 'isoformat', 'isoweekday', 
          'timetuple'] 
      for field in fields: 
        output[field] = getattr(obj, field) 
      for method in methods: 
        output[method] = getattr(obj, method)() 
      output['epoch'] = time.mktime(obj.timetuple()) 
      return output 

    elif isinstance(obj, time.struct_time): 
      return list(obj) 

    elif isinstance(obj, users.User): 
      output = {} 
      methods = ['nickname', 'email', 'auth_domain'] 
      for method in methods: 
        output[method] = getattr(obj, method)() 
      return output 

    return simplejson.JSONEncoder.default(self, obj) 

class AtomEncoder(object):
	def encode(self, obj):
		return obj

def json(input): 
	"""Encode an input GQL object as JSON 

    Args: 
      input: A GQL object or DB property. 

    Returns: 
      A JSON string based on the input object.  

    Raises: 
      TypeError: Typically occurs when an input object contains an unsupported 
        type. 
    """ 
	return GqlEncoder().encode(input)

def atom(input):
	return input
	# AtomEncoder().encode(input)
	
# xml
# from django.core import serializers
# data = serializers.serialize("xml", Photo.objects.all())