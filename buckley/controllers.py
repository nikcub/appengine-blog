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
  Buckley - Controllers
  
"""

import reqhandlers 
import logging
import datetime

from google.appengine.api import memcache
from models import Post

# @TODO get rid of this
existing_posts = [
  'blockplus-a-browser-extension-to-block-google-notifications', 
  'cutting-off-burners', 
  'facebook-fixes-logout-issue-explains-cookies', 
  'facebook-re-enables-controversial-tracking-cookie', 
  'fidelio-a-browser-plugin-for-secure-web-browsing', 
  'finding-a-technical-co-founder', 
  'frictionless-facebook-social-sharing-browser-plugin', 
  'google-android-the-accidental-empire', 
  'guide-to-finding-a-good-and-safe-company-or-product-name', 
  'howto-setup-secure-and-private-facebook-browsing', 
  'lies-damn-lies-and-google-statistics', 
  'logging-out-of-facebook-is-not-enough', 
  'numeronym', 
  'pain-and-gain', 
  'persistant-and-unblockable-cookies-using-http-headers', 
  'relevance-time-for-twitter', 
  'the-google-ipo-skeptics', 
  'unicode-uf8ff-aka-the-apple-logo-character-on-macs',
  'crunchpad-proof-obviousness-in-ipad-design',
  'google-firefox-chrome-lady-gaga',
  'how-megaupload-was-investigated-and-indicted',
  'facebook-is-losing-e-commerce',
  'facebook-also-doesnt-honor-p3p',
  'blockplus-v4-released-block-google-widgets-and-links-from-other-google-sites',
  'yahoo-axis-chrome-extension-leaks-private-certificate-file'
]

class About(reqhandlers.Base):
  def get(self, path=None):
    return self.render('about', {'tab_about': True})

class Contact(reqhandlers.Base):
  def get(self, path=None):
    return self.render('contact', {'tab_contact': True})

class Consulting(reqhandlers.Base):
  def get(self, path=None):
    self.render('consulting', {'tab_consulting': True})

class Projects(reqhandlers.Base):
  def get(self, path=None):
    self.render('projects', {'tab_projects': True})

class Feed(reqhandlers.Base):
  "Defines projects"
  def get(self, path):
    if not path:
      return self.redirect('http://feeds.feedburner.com/NewWebOrder', permanent=True)
    cached = self.request.get('cache', False)
    posts, src = Post.get_posts_published_cached(10, key='feed', cache=cached)
    self.render_feed('feed2', {
      'posts': posts,
      'src': src,
      'now': datetime.datetime.now(),
    })

class Archive(reqhandlers.Base):
  def get(self, when=None):
    if not when:
      when = 'all'
    # arch = 'month'
    # posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC LIMIT 10")
    posts = Post.get_posts_published(100)
    src = 'db'
    self.render('archive', {
      'posts': posts,
      'tab_archive': True,
      'src': src,
    })

class SinglePost(reqhandlers.Base):
  def get(self, title=None):
    self.render_error('File Not Found', 404)
    # post = Post.stub_exists(title)
    # if post:
      # self.render('single', { 'post': post,
        # 'tab_blog': True })
    # else:

class Blog(reqhandlers.Base):
  "Defines the main blog"
  def get(self, path):
    defaults = ['', '/', 'index', 'index.html', 'index.htm']
    host = self.request.environ['HTTP_HOST']
    cached_pages = ['logging-out-of-facebook-is-not-enough']
    referred_cache = self.request.get('ref', False)
    path_comp = path.split('/', 1)
    
    if path and path_comp[0] != 'posts' and path in existing_posts:
      return self.redirect('/posts/' + path, permanent=True)

    if path_comp[0] == 'posts':
      path = path_comp[1]
      
    if path == 'facebook-fixes-logout-issue':
      return self.redirect('http://' + host + '/' + 'facebook-fixes-logout-issue-explains-cookies', permanent=True)

    if host not in ['localhost:9090', 'localhost:8090', 'staging.nikcub.appspot.com', '5.nikcub.appspot.com', 'www.nikcub.com'] and not referred_cache:
      return self.redirect("http://www.nikcub.com/" + path, permanent=True)

    cache = self.request.get('cache', False)
    # 
    if not cache:
      page_cache = memcache.get('post.%s' % path)
      if page_cache:
        return self.render_content(page_cache)
    
    p, src = Post.stub_exists(path, cache)
    if p:
      # posts = Post.get_single_by_stub(path)
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
