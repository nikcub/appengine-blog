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
  buckley - application

"""

import logging
import os
import types

from google.appengine.ext.webapp import WSGIApplication

class AppAuthError(Exception):
  pass
  
class Application(WSGIApplication):

  _Application__debug = True

  _Plugins = {}

  def _init_plugin_class(self, plugin_name):
    fromlist = [plugin_name]
    try:
      module = __import__("plugins.%s.%s" % (plugin_name, plugin_name), globals(), {}, fromlist)
    except ImportError:
      module = __import__("plugins.%s" % (plugin_name), globals(), {}, fromlist)
      
    return getattr(module, plugin_name)()
  

  def _init_plugins(self, plugins):
    for plugin in plugins:
      # try:
      plug_inst = self._init_plugin_class(plugin)
      if plug_inst.set_config(plugins[plugin]):
        self._Plugins[plugin] = plug_inst
      # except ImportError, e:
        # logging.error('could not import pluging %s: %s' % (plugin, e))
      # except Exception, e:
        # logging.error('Exception: %s' % e)


  def __init__(self, url_mapping, plugins, debug=False):
    self._init_url_mappings(url_mapping)
    self._init_plugins(plugins)
    self.__debug = debug
    WSGIApplication.active_instance = self
    self.current_request_args = ()


  def __call__(self, environ, start_response):
    """Called by WSGI when a request comes in."""
    request = self.REQUEST_CLASS(environ)
    response = self.RESPONSE_CLASS()

    WSGIApplication.active_instance = self

    handler = None
    groups = ()
    for regexp, handler_class in self._url_mapping:
      match = regexp.match(request.path)
      if match:
        try:
          handler = handler_class()
          handler.initialize(request, response)
          if hasattr(handler, 'plugin_register'):
            for pl in self._Plugins:
              handler.plugin_register(pl, self._Plugins[pl])
          else:
            logging.error("Handler %s does not support plugin resitration" % handler.__name__)
          groups = match.groups()
          break
        except AppAuthError:
          logging.error('caught AppAuthError')
          response.set_status(403)
          handler = None

    self.current_request_args = groups
    
    if handler:
      try:
        method = environ['REQUEST_METHOD']
        if method == 'GET':
          handler.get(*groups)
        elif method == 'POST':
          handler.post(*groups)
        elif method == 'HEAD':
          handler.head(*groups)
        elif method == 'OPTIONS':
          handler.options(*groups)
        elif method == 'PUT':
          handler.put(*groups)
        elif method == 'DELETE':
          handler.delete(*groups)
        elif method == 'TRACE':
          handler.trace(*groups)
        else:
          handler.error(501)
      except Exception, e:
        handler.handle_exception(e, self.__debug)
    else:
      response.set_status(404)

    response.wsgi_write(start_response)
    return ['']
