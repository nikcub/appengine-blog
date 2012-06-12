#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:expandtab
#
# Copyright (c) 2012, Nik Cubrilovic. All rights reserved.
#
# <nikcub@gmail.com> <http://nikcub.appspot.com>  
#
# Licensed under a BSD license. You may obtain a copy of the License at
#
#     http://nikcub.appspot.com/bsd-license
#
"""
  Buckley - reqhandlers.py
  
  Base Request handlers used by controllers

"""

import os
import logging
import traceback
import sys
import cgi
import datetime

from vendor import jinja2
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache

from django.utils.timesince import timesince
from django.utils.dateformat import format as django_format

from config import config
import serialize
from application import AppAuthError

class Base(webapp.RequestHandler):
  
  _Plugins = {}
  
  def __init__(self):
    self.conf = config('blog.yaml')
  
  def plugin_register(self, plugin_name, plugin_inst):
    self._Plugins[plugin_name] = plugin_inst

  def render(self, template_name, vars, response_code = 200, response_type = False):
    content = self.get_page(template_name, vars, response_type)
    self.render_content(content, response_code)

  def render_feed(self, template_name, vars, response_code = 200, response_type = False):
    vars['buildDate'] = datetime.datetime.now()
    content = self.render_jinja(self.get_template_path(template_name, 'xml'), vars)
    headers = [('Content-Type', "application/%s; charset=utf-8" % ('xml'))]
    return self.render_content(content, response_code, headers)
        
  def render_error(self, message = False, code = 404):
    return self.render('error', { 
      'code': '%d - %s' % (code, self.response.http_status_message(code)), 
      'message': message 
    }, code)

  def render_content(self, content, response_code = 200, headers = []):
    self.response.clear()
    if len(headers) > 0:
      for hn, hv in headers:
        self.response.headers[hn] = hv
    self.response.set_status(response_code)
    self.response.out.write(content)
    
  def get_page(self, template_name, vars, response_type = False):
    if not response_type:
      response_type = self.get_response_type()
    vars = self.get_template_vars(vars)
    vars = self.get_plugin_vars(vars)
    if response_type in ['xml', 'json']:
      serial_f = getattr(serialize, response_type)
      content = serial_f(vars)
      self.response.headers['Content-Type'] = "application/%s; charset=utf-8" % (response_type)
    else:
      # content = template.render(self.get_template_path(template_name, response_type), vars)
      content = self.render_jinja(self.get_template_path(template_name, response_type), vars)
    return content

  def get_plugin_vars(self, vars):
    for plugin in self._Plugins:
      if hasattr(self._Plugins[plugin], "render"):
        val_dict = self._Plugins[plugin].render()
        if type(val_dict) == type({}):
          for temp_var in val_dict:
            if not vars.has_key(temp_var):
              vars[temp_var] = val_dict[temp_var]
        else:
          logging.error("Did not get a valid dict type from plugin %s" % plugin)
    return vars

  def get_template_vars(self, vars):
    
    host_full = self.request.environ['HTTP_HOST'] or 'localhost'
    hostname = host_full.split(':')[0]
    
    if hostname == 'localhost':
      stat_hosts = [host_full]
      css_file = 'nikcub.min.css'
    else:
      stat_hosts = ['nik-cubrilovic.appspot.com', 'sketch-proto.appspot.com', 'hterms.appspot.com']
      css_file = 'nikcub.027.min.css'

    additional = {
      'admin': users.is_current_user_admin(),
      'user': users.get_current_user(),
      'logout': users.create_logout_url('/'),
      'login': users.create_login_url('/'),
      'static_host': 'static.nikcub.com',
      'css_file': 'nikcub.030.min.css',
      'css_ver': '31',
      'src': 'database',
      # 'title': self.conf_get('title')
    }
    return dict(zip(additional.keys() + vars.keys(), additional.values() + vars.values()));

  def render_jinja(self, template_path, template_vars):
    # Split the full path as needed for Jinja
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)
    #  and run it
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    # from sketch.utils import timesince
    env.filters['timesince'] = timesince
    env.filters['tformat'] = django_format
    jinja_template = env.get_template(template_name)
    return jinja_template.render(template_vars)

  def render_django(self, template_path, template_vars):
    """
      render a django template
      
      TODO: convert to use_library()
    """
    return django_template.render(template_path, template_vars)


  def render_cache(self, template_name, vars):
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', template_name + '.html')
    content = self.render_django(template_path, self.get_template_vars(vars))
    return content

  def get_template_path(self, template_name, template_format = 'html'):
    return os.path.join(os.path.dirname(__file__), '..', 'templates', template_name + '.' + template_format)
  
  def get_response_type(self):
    if not self.request.headers.has_key('accept'):
      return 'html'
      
    accept = self.request.headers['accept'].split(',')
    if accept[0] == 'application/json' or self.request.get('json'):
      return 'json'
    elif self.request.get('xml'):
      return 'xml'
    else:
      return 'html'
  
  def get_param_dict(self):
    params = {}
    for argument in self.request.arguments():
      params[argument] = self.request.get(argument)
    return params

  def handle_exception(self, exception, debug_mode):
    logging.exception(exception)
    message = "An error has occured"
    if debug_mode:
      lines = ''.join(traceback.format_exception(*sys.exc_info()))
      message = '<pre>%s</pre>' % (cgi.escape(lines, quote=True))
    self.render_error(message, 500)

  def slugify(self, value):
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


class Admin(Base):
  def initialize(self, request, response):
    self.request = request
    self.response = response
    user = users.get_current_user()
    is_admin = users.is_current_user_admin()
    if user == None or is_admin != True:
      login_url = users.create_login_url('/admin')
      raise AppAuthError('login required')
      return False
      
  def is_admin():
    return users
    
  def get_template_path(self, template_name, template_format = 'html'):
    return os.path.join(os.path.dirname(__file__), 'templates', template_name + '.' + template_format)
  