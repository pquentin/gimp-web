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
import getopt
import os
import re
import string
import sys
import time
import types

sys.path = ['${LIBDIR}'] + sys.path

import xhtml
import wgo
import wgo_news
import wgo_queue

def main():
  form = cgi.FieldStorage()

  #wgo.config.debug = True
  
  if wgo.config.debug: xhtml.print_form(form)

  if not (form.has_key("message-id") and form.has_key("action") and form.has_key("queue")) and not (form.has_key("subject") and form.has_key("body")):
    wgo_news.header()
    wgo_news.footer(wgo.error("Malformed http request."))
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

  try:
    news = wgo_news.news(form)
  except:
    wgo_news.header()
    wgo_news.footer(wgo.error("The news article is malformed.  Check the date, it should be <i>day month year hour:minute:seconds</i> GMT  Perhaps it is missing a subject line, or it has no body.  "))
    return (-1)
    

  if action == "save":
    news.to_queue(queue)
    link = xhtml.hyperlink("Continue", { "href" : "news-edit.cgi?message-id=%s&queue=%s" % (news["message-id"], queue)})
    status = "success"
    goto = ["Location: news-edit.cgi?message-id=%s&queue=%s" % (xhtml.escape(news["message-id"]), queue)]
  elif action == "approve":
    news.to_queue(wgo_news.config.current_queue)
    if os.path.exists(wgo_queue.message_path(queue, news["message-id"])):
      os.remove(wgo_queue.message_path(queue, news["message-id"]))
      pass
    
    link = xhtml.hyperlink("Continue", { "href" : "news-index.cgi?%s" % (queue)})
    status = "success"
    goto = ["Location: news-index.cgi?%s" % (queue)]
  elif action == "disapprove":
    news.to_queue(wgo_news.config.pending_queue)
    if os.path.exists(wgo_queue.message_path(queue, news["message-id"])):
      os.remove(wgo_queue.message_path(queue, news["message-id"]))
      pass
    
    link = xhtml.hyperlink("Continue", {"href" : "news-index.cgi?%s" % (queue)})
    status = "success"
    goto = ["Location: news-index.cgi?%s" % (queue)]
  elif action == "archive":
    news.to_queue(wgo_news.config.archive_queue)
    if os.path.exists(wgo_queue.message_path(queue, news["message-id"])):
      os.remove(wgo_queue.message_path(queue, news["message-id"]))
      pass
    
    link = xhtml.hyperlink("Continue", {"href" : "news-index.cgi?%s" % (queue)})
    status = "success"
    goto = ["Location: news-index.cgi?%s" % (queue)]
  elif action == "delete":
    if os.path.exists(wgo_queue.message_path(queue, news["message-id"])):
      os.remove(wgo_queue.message_path(queue, news["message-id"]))
      pass
    
    link = xhtml.hyperlink("Continue", {"href" : "news-index.cgi?%s" % (queue)})
    status = "success"
    goto = ["Location: news-index.cgi?%s" % (queue)]
  else:
    link = xhtml.hyperlink("Restart", {"href" : "index.html"})
    queue = ""
    status = "failed"
    pass

  if status == "success":
     print goto[0]
     print
  else:
    wgo_news.header()
    wgo_news.footer(wgo.error(string.capitalize(action) + " " + string.capitalize(status)))
    pass
    
  return (0)

sys.exit(main())
