#!/usr/bin/env ${PYTHON}
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
import calendar
import types

sys.path = ['${LIBDIR}'] + sys.path

import wgo
import wgo_admin
import rdf
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

  def __init__(self, source=None, raise_exception=True):
    self.valid = False

    try:
      if source == None:
        self.msg = email.Message.Message()
        self.msg["Date"] = rfc822.formatdate()
        self.msg["From"] = "<wilber@news.gimp.org> Wilber Gimp"
        self.msg["Message-Id"] = "<" + time.strftime("%Y%m%d%H%M%S-") + str(os.getpid()) + "@news.gimp.org>" 
        self.msg["Reply-To"] = ""
        self.msg["Subject"] = "(none)"
        self.msg[news.editor_header] = ""
        self.msg[news.image_header] = "--none--"
        self.msg.set_payload("")
        self.msg.epilogue = ""
        self.valid = True
      elif str(source.__class__) == 'cgi.FieldStorage':
        self.msg = email.Message.Message()
        self.msg["Date"] = rfc822.formatdate(calendar.timegm(rfc822.parsedate(xhtml.unescape(source["date"].value))))
        self.msg["From"] = xhtml.unescape(source["from"].value)
        self.msg["Message-Id"] = xhtml.unescape(source["message-id"].value)
        self.msg["Reply-To"] = ""
        self.msg["Subject"] = xhtml.unescape(source["subject"].value)
        self.msg[news.editor_header] = xhtml.unescape(source["editor"].value)
        self.msg[news.image_header] = xhtml.unescape(source["image"].value)
        self.msg.set_payload(source["body"].value)
        self.msg.epilogue = ""
        self.valid = True
      elif str(source.__class__) == "<type 'str'>":
        if source.endswith('news-blotter') or source.endswith('news.rdf'):
          self.valid = False
        else:
          fd = open(source, "r")
          self.msg = email.message_from_file(fd)
          fd.close()
          self.valid = True
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
      pass
    except:
      self.valid = False
      if raise_exception:
        raise ValueError
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

       
  def as_news_item(self):               # As a line in the blotter
    iso_date = time.strftime(config.datetime_format, rfc822.parsedate(self["date"]))

    s = str(xhtml.comment("$Id$")) + str(xhtml.span(xhtml.quote(self["subject"]), {"class" : "newstitle"})
                      + xhtml.span(xhtml.quote(iso_date), {"class" : "newsdate"}))

    s = xhtml.h1(s + "&nbsp;", {"class" : "newsheading"})

    img = ""
    if icon_by_name(self["image"]) != "":
      img = xhtml.image({"src" : config.icon_dir + icon_by_name(self["image"]), "alt" : icon_desc_by_name(self["image"])})
      pass

    s += str(xhtml.div(img + as_para(self["body"]), {"class" : "news"}))

    return (s)


  def as_rdf(self):
    http_host = config.default_http_host
    if os.environ.has_key("HTTP_HOST"):
      http_host = os.environ["HTTP_HOST"]
      pass

    date = rfc822.formatdate(time.mktime(rfc822.parsedate(xhtml.unescape(self["date"]))))
    s = rdf.item(rdf.title(rdf.quote(self["subject"]))
                 + rdf.description(rdf.quote(xhtml.absolutize(self["body"],
                                                              "http://" + http_host)))
                 + "\n"
                 + rdf.link("http://" + http_host)
                 + "\n"
                 + rdf.pubDate(rdf.quote(date)))
    return (s)

  
  def to_queue(self, queue):
    filename = wgo_queue.message_path(queue, self["message-id"])
    fp = open(filename, "w")
    print >>fp, self.msg
    fp.close()
    os.chmod(filename, config.news_permission)
    wgo_queue.generate_blotter(queue)
    return (0)


  def from_queue(self, queue):
    filename = wgo_queue.message_path(queue, self["message-id"])
    if os.path.exists(filename):
      os.remove(filename)
      wgo_queue.generate_blotter(queue)
      pass
    return (0)

  pass
  
################################################################################

def header():
  wgo.http_preamble(["Content-type: text/html"])

  #  wgo_admin.header("www.gimp.org - Administration",
  #                   [ {"rel" : "stylesheet", "href" : config.news_dir + "/news-admin.css", "type" : "text/css", "media" : "screen"} ])
  wgo_admin.header("www.gimp.org - Administration")

  return

def footer(prefix=None):
  return (wgo_admin.footer(prefix))

icons = {
  "--none--"                   : "",             # must be present
  "Default"                    : "gimp_construction.png", # must be present
  "Developer"                  : "gimp_code.png",
  "Developer Release"          : "release-dev.png",
  "Release"                    : "release-0.1.png",
  "Wilber the Painter"         : "wilber_painter.png",
  "Wilber the Wizard"          : "wilber_wizard.png",
  "Wilber the Painter Builder" : "wilber_work.png",
  "Wilber Reading"             : "wilber_reading.png",
  "Wilber Shocked"             : "wilber_eeek.png"
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

# Must match the names in "icons" above
icon_descs = {
  "--none--"          : "",
  "Default"           : "[?]",
  "construction"      : "[Wilber the Builder]",
  "developer"         : "[Developers]",
  "developer-release" : "[Developer Release]",
  "release"           : "[Release]",
  "wilber_painter"    : "[Wilber the Painter]",
  "wilber_wizard"     : "[Wilber the Wizard]",
  "wilber_work"       : "[Wilber the Painting Builder]",
  "wilber_reading"    : "[Wilber Reading]",
  "wilber_eeek"       : "[Wilber Shocked]"
}

def icon_desc_by_name(name):
  if icon_descs.has_key(name):
    return (icon_descs[name])
  return (icon_descs["Default"])

# Embeds body in para element, but only if needed (FIXME: should be smarter)
def as_para(body):
  if body[:3] != '<p>':
    return xhtml.para(body)
  return body
