#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, logging, reqhandlers 
from models import *
from vendor.BeautifulSoup import BeautifulStoneSoup
    
table_feed = "http://www.footbo.com/widgets/xml/LeagueTable.aspx?id=193698&LANGUAGE=en-US&GIGYA=true"
fixtures_feed_full = "http://soccernet.espn.go.com/scores?date=20110813&league&cc=3436&xhr=1"

LEAGUES = {
  "EPL": "English Premier League"
}

class SoccerGen(reqhandlers.Base):
  "soccer generator"
  def parse_fixtures(self, league="EPL"):
    ff_path = os.path.join(os.path.dirname(__file__), 'socgen', 'test.html')
    if not os.path.exists(ff_path):
      return "Path Error: %s" % ff_path
    ff = open(ff_path, 'r')
    fix_bs = BeautifulStoneSoup(ff)
    
    logging.info(ff)
    logging.info(fix_bs.prettify())
    
    return fix_bs.prettify()

  def get(self):
    self.date = datetime.datetime.utcnow()
    self.date_short = self.date.strftime('%Y%m%d')
    
    self.f_raw = self.parse_fixtures()
    
    return self.render('soccer-gen', {
      'date': self.date,
      'date_short': self.date_short,
      'ff_raw': self.f_raw,
    })

