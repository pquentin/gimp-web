#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-
#
# www.gimp.org website administration and tools
#
# Copyright (C) 2002, 2003 Helvetix Victorinox, a pseudonym,
# Mountain View, California
# 
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import email
import email.MIMEMessage
import cgi
import errno
import fcntl
import getopt
import mimetypes
import os
import re
import rfc822
import stat
import string
import sys
import time
import types

import wgo
import wgo_news
import news_config

def safe_filename(path):
  path = str(path)
  return (path.replace("/", "").replace("&", ""))

def canonical_path(qname):
  if qname in [ news_config.pending_queue, news_config.current_queue, news_config.archive_queue]:
    return (wgo.config.spool_path + qname + "/")
  return (None)

def file_path(qname, file):
  return canonical_path(qname) + safe_filename(file)
  
def message_path(qname, messageid):
  return (file_path(qname, messageid))
  
def generate_blotter(queue):
  dirpath = canonical_path(queue)

  if dirpath != None:
    names = map(lambda t: dirpath + t, os.listdir(dirpath))
    names.sort(lambda a, b: cmp(os.stat(a)[stat.ST_MTIME], os.stat(b)[stat.ST_MTIME]))
    news_items = filter(lambda n: n.valid, map(wgo_news.news, names))
             
    news_blotter = file_path(queue, news_config.news_blotter)
    
    fp_out = open(news_blotter, "w")
    print >>fp_out, "<!-- begin chartae -->"
    map(lambda n: fp_out.write(n.as_news_item()), news_items)
    print >>fp_out, "<!-- end chartae -->"
    fp_out.close()

    try:
      os.chmod(news_blotter, 0666)
      os.chown(news_blotter, wgo.config.user_uid)
    except:
      pass
    pass
  
  return (news_blotter)
