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

import cgi
import cgitb; cgitb.enable()
import errno
import fcntl
import getopt
import os
import re
import rfc822
import string
import sys
import time
import types

sys.path.append('${LIBDIR}')

import xhtml
import wgo
import wgo_news
import wgo_queue

print "Content-type: text/html"

wgo_news.header()

form = cgi.FieldStorage()

queue = ""
action = ""

if wgo.config.debug:
  xhtml.print_form(form)
  pass

if form.has_key("queue"):
  if form["queue"].value in ["pending", wgo_news.config.pending_queue]:
    queue = wgo_news.config.pending_queue
  elif form["queue"].value in ["current", wgo_news.config.current_queue]:
    queue = wgo_news.config.current_queue
  elif form["queue"].value in ["archive", wgo_news.config.archive_queue]:
    queue = wgo_news.config.archive_queue
    pass
  pass

if form.has_key("action"):
  action = string.lower(form["action"].value)
  pass

if queue == "" or action == "":
  print wgo_news.error("Malformed request")
  wgo_news.footer()
  sys.exit(1)
  pass
    

print xhtml.table.init({"class" : "batch"})
print xhtml.table.row(xhtml.table.header("Action") + xhtml.table.header("Message-Id") + xhtml.table.header("Status"))

for key in form.keys():
  if not key in ["queue", "action"]:
    message_id = xhtml.unescape(key)
    print xhtml.table.row.init()
    print xhtml.table.cell(action)
    print xhtml.table.cell(xhtml.quote(message_id))
      
    if action == "save":
      status = 0
    elif action in ["approve", "current"]:
      try:
        os.rename(wgo_queue.message_path(queue, message_id), wgo_queue.message_path(wgo_news.config.current_queue, message_id))
        status = 0
      except OSError, e:
        status = e.strerror
        pass
      pass
    elif action == "archive":
      try:
        os.rename(wgo_queue.message_path(wgo_news.config.current_queue, message_id), wgo_queue.message_path(wgo_news.config.archive_queue, message_id))
        status = 0
      except OSError, e:
        status = e.strerror
        pass
      pass
    elif action in ["disapprove", "unapprove", "pending"]:
      try:
        os.rename(wgo_queue.message_path(queue, message_id), wgo_queue.message_path(wgo_news.config.pending_queue, message_id))
        status = 0
      except OSError, e:
        status = e.strerror
        pass
      pass
    elif action == "delete":
      try:
        os.remove(wgo_queue.message_path(queue, message_id))
        status = 0
      except OSError, e:
        status = e.strerror
        pass
      pass
    elif action == "reject":
      status = "Reject unimplemented"
      pass
    else:
      status = "Bad action: " + form["action"].value
      pass
            
    if status == 0:
      print xhtml.table.cell("Successful", {"id" : "success"})
    else:
      print xhtml.table.cell(status, {"id" : "failure"})
      pass
        
    print xhtml.table.row.fini()
    pass
  pass

print xhtml.table.fini()

wgo_queue.generate_blotter(wgo_news.config.archive_queue)
wgo_queue.generate_blotter(wgo_news.config.current_queue)
wgo_queue.generate_blotter(wgo_news.config.pending_queue)

print xhtml.para(xhtml.hyperlink("Continue", { "href" : "news-index.cgi?%s" % (queue)}))

wgo_news.footer()
            
sys.exit(1)
