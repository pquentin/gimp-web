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

def main():
  form = cgi.FieldStorage()

  print "Content-type: text/html"

  wgo_news.head_boilerplate()

  if wgo_news.config.debug:
    print '<div style="border: thin solid red; font-size: small; padding: 2px;">'
    cgi.print_form(form)
    print '</div>'
    pass

  if not (form.has_key("message-id") and form.has_key("subject")) and form.has_key("body"):
    print xhtml.div("Error", {"class" : "heading"})
    wgo_news.foot_boilerplate()
    return (-1)

  news = wgo_news.news_from_form(form)

  action = ""
  if form.has_key("action"):
    action = string.lower(form["action"].value)
    pass

  if action != "" and form.has_key("queue"):
    if form["queue"].value == wgo_news.config.pending_queue:
      queue = wgo_news.config.pending_queue
    elif form["queue"].value == wgo_news.config.current_queue:
      queue = wgo_news.config.current_queue
    elif form["queue"].value == wgo_news.config.archive_queue:
      queue = wgo_news.config.archive_queue
    else:
      action = ""
      pass
    pass

  if action == "save":
    wgo_news.news_to_file(news, queue)
    link = xhtml.hyperlink("Continue",
                           { "href" : "news-edit.cgi?message-id=%s&queue=%s"
                             % (news["message-id"], queue)})
    status = "success"
  elif action == "approve":
    fp = open(wgo_news.config.current_queue + "/" + news["message-id"], "w")
    print >>fp, news
    fp.close()
    os.unlink(queue + "/" + news["message-id"])
    link = xhtml.hyperlink("Continue",
                           { "href" : "news-index.cgi?%s" % (queue)})
    status = "success"
    
  elif action == "disapprove":
    fp = open(wgo_news.config.pending_queue + "/" + news["message-id"], "w")
    print >>fp, news
    fp.close()
    os.unlink(queue + "/" + news["message-id"])
    link = xhtml.hyperlink("Continue",
                           { "href" : "news-index.cgi?%s" % (queue)})
    status = "success"
    
  elif action == "archive":
    fp = open(wgo_news.config.archive_queue + "/" + news["message-id"], "w")
    print >>fp, news
    fp.close()
    os.unlink(queue + "/" + news["message-id"])
    link = xhtml.hyperlink("Continue",
                           { "href" : "news-index.cgi?%s" % (queue)})
    status = "success"
    
  elif action == "delete":
    print "unlink:", queue + "/" + news["message-id"]
    try:
      os.unlink(queue + "/" + news["message-id"])
    except:
      pass
    link = xhtml.hyperlink("Continue",
                           { "href" : "news-index.cgi?%s" % (queue)})
    status = "success"
    
  elif action == "reject":
    print "reject not implemented"
    link = xhtml.hyperlink("Continue",
                           { "href" : "news-index.cgi?%s" % (queue)})
    status = "success"

  else:
    wgo_news.error("Malformed request")
    link = xhtml.hyperlink("Restart", { "href" : "index.html"})
    queue = ""
    status = "failed"
    pass
  
  print '<div class="subtitle">%s %s</div>' % (string.capitalize(action),
                                               string.capitalize(status))

  if link != "":
    print xhtml.para(link)
    pass

  if queue != "":
    wgo_news.news_generate_blotter(queue)
    pass
  
  if wgo_news.config.validator != 0:
    print xhtml.validate()
    
  wgo_news.foot_boilerplate()
    
  return (0)

sys.exit(main())
