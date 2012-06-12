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
  Buckley - main

  Simpel blog and CMS for appengine
"""

import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vendor'))

from google.appengine.dist import use_library
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from buckley import controllers
from buckley import admin
from buckley import projects
from buckley.application import Application

use_library('django', '0.96')

routes = [
	('/feed(.*)', controllers.Feed),
	('/about', controllers.About),
	('/contact', controllers.Contact),
	('/consulting', controllers.Consulting),
	('/projects', controllers.Projects),
	('/archive', controllers.Archive),
	('/admin/posts/(.*)/(.*)', admin.Posts),
	('/admin/posts/(.*)', admin.Posts),
	('/admin/posts', admin.Posts),
	('/admin/export', admin.Export),
	('/admin/export/(.*)', admin.Export),
	('/admin/cache', admin.Cache),
	('/admin/cache_page/(.*)', admin.CacheView),
	('/admin/pages/(.*)/(.*)', admin.Pages),
	('/admin/pages/(.*)', admin.Pages),
	('/admin/pages', admin.Pages),
	('/admin/settings', admin.Settings),
	('/admin(.*)', admin.Settings),
	('/password-gen', projects.PasswordGen),
	('/tracking-cookie', projects.TrackingCookie),
	('/(.*)', controllers.Blog)
]

plugins = {
	'most_recent': {
		'display_last': 10
		# 'css_class': 'sidebar_mr'
	},
	'disqus': {
		'site_id': 'nikcub'
	}
}

def main():
	app = Application(routes, plugins, debug=False)
	run_wsgi_app(app)

if __name__ == '__main__':
	main()
