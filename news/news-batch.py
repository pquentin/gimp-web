#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-
#
import cgi
import cgitb; cgitb.enable()
import email
import errno
import fcntl
import getopt
import mimetypes
import os
import re
import rfc822
import string
import sys
import time
import types

sys.path.append('__LIBDIR__')

import xhtml
import wgo_news

print "Content-type: text/html"

wgo_news.head_boilerplate()

form = cgi.FieldStorage()

queue = ""
action = ""

if wgo_news.config.debug:
  print '<div style="border: thin solid red; font-size: small; padding: 2px;">'
  cgi.print_form(form)
  print '</div>'
  pass


if form.has_key("queue"):
  if form["queue"].value == wgo_news.config.pending_queue:
    queue = wgo_news.config.pending_queue
  elif form["queue"].value == wgo_news.config.current_queue:
    queue = wgo_news.config.current_queue
  elif form["queue"].value == wgo_news.config.archive_queue:
    queue = wgo_news.config.archive_queue
    pass
  pass


if form.has_key("action"):
  action = string.lower(form["action"].value)
  pass

if queue == "" or action == "":
  print wgo_news.error("Malformed request")
  wgo_news.foot_boilerplate()
  sys.exit(1)
  pass
    

print xhtml.table.init({"class" : "news", "width" : "100%", "cellpadding" : "0", "cellspacing" : "0"})

attrs = { "class" : "news" }
print xhtml.table.row(xhtml.table.header("Action", attrs)
                      + xhtml.table.header("Message-Id", attrs)
                      + xhtml.table.header("Status", attrs), attrs)

for k in form.keys():
  if k != "queue":
    x = string.replace(k, queue + "/", "")
    if x != k:
      message_id = x
      print xhtml.table.row.init(attrs)
      print xhtml.table.cell(action, attrs)
      print xhtml.table.cell(message_id, attrs)
            
      if action == "save":
        status = 0
      elif action == "approve" or action == "current":
        status = os.system("/bin/mv -f '%s/%s' '%s/%s'" % (queue, message_id, wgo_news.config.current_queue, message_id))
      elif action == "archive":
        status = os.system("/bin/mv -f '%s/%s' '%s/%s'" % (wgo_news.config.current_queue, message_id, wgo_news.config.archive_queue, message_id))
      elif action == "disapprove" or action == "unapprove" or action == "pending":
        status = os.system("/bin/mv -f '%s/%s' '%s/%s'" % (queue, message_id, wgo_news.config.pending_queue, message_id))
      elif action == "delete":
        status = os.unlink("%s/%s" % (queue, message_id))
      elif action == "reject":
        status = 0
        pass
      else:
        print xhtml.table.cell("bad action '%s'" % (form["action"].value), attrs)
        status = 1
        pass
            
      if status == 0:
        print xhtml.table.cell("Successful", attrs)
      else:
        print xhtml.table.cell("Failed", {"style" : "background-color: \#ff8080;"})
        pass
        
      print xhtml.table.row.fini()
      pass
    pass
  pass

print xhtml.table.fini()

wgo_news.news_generate_blotter(wgo_news.config.archive_queue)
wgo_news.news_generate_blotter(wgo_news.config.current_queue)
wgo_news.news_generate_blotter(wgo_news.config.pending_queue)

link = xhtml.hyperlink("Continue", { "href" : "news-index.cgi?%s" % (queue)})

print xhtml.para(link)

if wgo_news.config.validator != 0:
  print xhtml.validate()
    
wgo_news.foot_boilerplate()
            
sys.exit(1)
