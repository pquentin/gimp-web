#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-
#
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
import wgo
import wgo_news
import wgo_queue

def main():
  form = cgi.FieldStorage()

  if wgo.config.debug: xhtml.print_form(form)

  if not (form.has_key("message-id") and form.has_key("action") and form.has_key("queue")) and not (form.has_key("subject") and form.has_key("body")):
    wgo_news.header()
    wgo.error("Malformed request")
    wgo_news.footer()
    return (-1)
  
  action = string.lower(xhtml.unescape(form["action"].value))

  queue = xhtml.unescape(form["queue"].value)
    
  if queue in ["pending", wgo_news.config.pending_queue]:
    queue = wgo_news.config.pending_queue
  elif queue in ["current", wgo_news.config.current_queue]:
    queue = wgo_news.config.current_queue
  elif queue in ["archive", wgo_news.config.archive_queue]:
    queue = wgo_news.config.archive_queue
  else:
    action = ""
    queue = ""
    pass

  news = wgo_news.news(form)

  if action == "save":
    news.to_queue(queue)
    link = xhtml.hyperlink("Continue", { "href" : "news-edit.cgi?message-id=%s&queue=%s" % (xhtml.escape(news["message-id"]), queue)})
    status = "success"
    #status = "failed"
  elif action == "approve":
    news.to_queue(wgo_news.config.current_queue)
    os.remove(wgo_queue.message_path(queue, news["message-id"]))
    link = xhtml.hyperlink("Continue", { "href" : "news-index.cgi?%s" % (queue)})
    status = "success"
  elif action == "disapprove":
    news.to_queue(wgo_news.config.pending_queue)
    os.remove(wgo_queue.message_path(queue, news["message-id"]))
    link = xhtml.hyperlink("Continue", {"href" : "news-index.cgi?%s" % (queue)})
    status = "success"
  elif action == "archive":
    news.to_queue(wgo_news.config.archive_queue)
    os.remove(wgo_queue.message_path(queue, news["message-id"]))
    link = xhtml.hyperlink("Continue", {"href" : "news-index.cgi?%s" % (queue)})
    status = "success"
  elif action == "delete":
    try: os.remove(wgo_queue.message_path(queue, news["message-id"]))
    except:
      pass
    link = xhtml.hyperlink("Continue", {"href" : "news-index.cgi?%s" % (queue)})
    status = "success"
  else:
    link = xhtml.hyperlink("Restart", {"href" : "index.html"})
    queue = ""
    status = "failed"
    pass

  if status == "success":
    wgo_news.header(["Location: news-edit.cgi?message-id=%s&queue=%s" % (xhtml.escape(news["message-id"]), queue)])

    #print xhtml.div(string.capitalize(action) + " " + string.capitalize(status), {"class" : "subtitle"})
    #if link != "": print xhtml.para(link)
    #if queue != "": wgo_queue.generate_blotter(queue)
    #wgo_news.footer()
  else:
    wgo_news.header()
    print wgo.error(string.capitalize(action) + " " + string.capitalize(status))
    wgo_news.footer()
    pass
    
  return (0)

sys.exit(main())
