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
import xhtml
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
import wgo_queue
import news_config as config

def re_substr(regex, str):
  if str != None:
    regex = re.compile(regex).search(str, 0)
    if regex != None:
      return regex.expand("\\1")
    pass
    
  return None

class news:
  image_header = "X-wgo-image"
  editor_header = "X-wgo-editor"

  def __init__(self, source=None):
    self.valid = False

    if source == None:
      self.msg = email.Message.Message()
      self.msg["Date"] = rfc822.formatdate(time.mktime(time.gmtime()))
      self.msg["From"] = "<wilber@news.gimp.org> Wilber Gimp"
      self.msg["Message-Id"] = "<" + time.strftime("%Y%m%d%H%M%S-") + str(os.getpid()) + "@news.gimp.org>" 
      self.msg["Reply-To"] = ""
      self.msg["Subject"] = "(none)"
      self.msg[news.editor_header] = ""
      self.msg[news.image_header] = ""
      self.msg.set_payload("")
      self.msg.epilogue = ""
      self.valid = True
    elif str(source.__class__) == 'cgi.FieldStorage':
      self.msg = email.Message.Message()
      self.msg["Date"] = rfc822.formatdate(time.mktime(rfc822.parsedate(xhtml.unescape(source["date"].value))))
      self.msg["From"] = xhtml.unescape(source["from"].value)
      self.msg["Message-Id"] = xhtml.unescape(source["message-id"].value)
      self.msg["Reply-To"] = ""
      self.msg["Subject"] = xhtml.unescape(source["subject"].value)
      self.msg[news.editor_header] = xhtml.unescape(source["editor"].value)
      self.msg[news.image_header] = xhtml.unescape(source["image"].value)
      self.msg.set_payload(xhtml.unescape(source["body"].value))
      self.msg.epilogue = ""
      self.valid = True
    elif str(source.__class__) == "<type 'str'>":
      try:
        fd = open(source, "r")
        self.msg = email.message_from_file(fd)
        fd.close()
        self.valid = True
      except:
        pass
      pass
    elif str(source.__class__) == 'email.Message.Message':
      self.msg = source
      self.valid = True
      pass
    else:
      self.valid = False
      pass

    if hasattr(self, 'msg'):
      if not self.msg.has_key(news.image_header): self.msg[news.image_header] = ""
      if not self.msg.has_key(news.editor_header): self.msg[news.editor_header] = ""
      pass
    
    return (None)

    
  def __getitem__(self, name):
    if string.lower(name) == "date":         return self.msg.get("Date")
    elif string.lower(name) == "image":      return self.msg.get(news.image_header)
    elif string.lower(name) == "editor":     return self.msg.get(news.editor_header)
    elif string.lower(name) == "subject":    return self.msg.get("subject")
    elif string.lower(name) == "message-id": return self.msg.get("message-id")
    elif string.lower(name) == "from":       return self.msg.get("from")
    elif string.lower(name) == "body":
      if self.msg.is_multipart():
        part = self.msg.get_payload(0)
        return (part.get_payload())
      else:
        return (self.msg.get_payload())
    
    return self.msg.get(name)
    
  def __setitem__(self, name, value):
    if string.lower(name) == "message-id": del self.msg["Message-Id"];       self.msg["Message-Id"] = value
    elif string.lower(name) == "from":     del self.msg["From"];             self.msg["From"] = value
    elif string.lower(name) == "subject":  del self.msg["Subject"];          self.msg["Subject"] = value
    elif string.lower(name) == "image":    del self.msg[news.image_header];  self.msg[news.image_header] = value
    elif string.lower(name) == "editor":   del self.msg[news.editor_header]; self.msg[news.editor_header] = value
    elif string.lower(name) == "date":     del self.msg["Date"];             self.msg["Date"] = value
    elif string.lower(name) == "body":
      self.msg.set_payload(value)
      pass
      
    return (self)
       
  def as_news_item(self):               # As a line in the index
    iso_date = time.strftime(config.datetime_format, rfc822.parsedate(self["date"]))

    s = str(xhtml.div(xhtml.span(xhtml.quote(self["subject"]), {"class" : "newstitle"})
                      + xhtml.span(xhtml.quote(iso_date), {"class" : "newsdate"})
                      + "&nbsp;", {"class" : "newsheading"}))

    s += str(xhtml.para(xhtml.image({"src" : config.icon_dir + icon_by_name(self["image"]), "alt" : self["image"]}) + self["body"],
                        {"class" : "news"}))
    return (s)

  def to_queue(self, queue):
    fp = open(wgo_queue.message_path(queue, self["message-id"]), "w")
    print >>fp, self.msg
    fp.close()
    return (0)

  pass
  
################################################################################

def header(headers=[]):
  headers = headers + ["Content-type: text/html"]
  for h in headers: print h
  print
  
  return (wgo.header("www.gimp.org - Administration", [config.news_dir + "/news-admin.css"], wgo.config.DocumentRoot_path + '/includes/admin-menu.inc'))

def footer():
  return (wgo.footer())


icons = {
  "--none--"          : "",         # must be present
  "Default"           : "gimp_construction.png", # must be present
  "construction"      : "gimp_construction.png",
  "developer"         : "gimp_code.png",
  "developer-release" : "release-dev.png",
  "release"           : "release-0.1.png"
}

def icon_option_list(selected):
  options = ""

  keys = icons.keys()
  keys.sort()
  
  for k in keys:
    attrs = {"value" : k}
    if k == selected:
      attrs.update({"selected" : "selected"})
    options += "%s" % (xhtml.input.option(k, attrs))
    pass
  
  return (options)

def icon_by_name(name):
  if icons.has_key(name):
    return (icons[name])
  return (icons["Default"])