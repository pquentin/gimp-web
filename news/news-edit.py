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
import sha
import string
import sys
import time
import types

sys.path.append('__LIBDIR__')

import xhtml
import wgo_news

def load_icons_as_options(selected):
  options = ""

  try:
    fp = open(wgo_news.config.news_icon_path + "options.txt")
    for l in fp.readlines():
      f = string.split(l)

      if f[1] == selected:
        attrs = {"value" : f[1], "selected" : "selected"}
      else:
        attrs = {"value" : f[1]}
        pass
      
      options += "%s" % (xhtml.input.option(f[0], attrs))
      pass
    
    fp.close()
  except:
    options = "%s" % (xhtml.input.option("no icons installed", {"value" : f[1],
                                                                "selected" : "selected"}))
    pass
  
  return (options)

# produce one page per pending news item.
# some sanity checking ought to be done to limit message sizes.
def html_news_edit(this_queue, other_queue, news_item, editor):
  
  if this_queue == wgo_news.config.pending_queue and other_queue == wgo_news.config.current_queue:
    approve_disapprove = xhtml.input.submit({"name" : "action",
                                             "value" : "approve",
                                             "class" : "submit-button"})
    pass
  elif this_queue == wgo_news.config.current_queue and other_queue == wgo_news.config.pending_queue:
    approve_disapprove = xhtml.input.submit({"name" : "action",
                                             "value" : "disapprove",
                                             "class" : "submit-button"})
    pass
  else:
    approve_disapprove = ""
    pass


  image_selector = xhtml.input.select(load_icons_as_options(news_item.props["image"]),
                                      { "class" : "news-edit",
                                        "name"  : "image"})

  print xhtml.div("GIMP ORG News Administration :: EDIT %s ITEM" % (string.upper(this_queue)), {"class" : "heading"})

  print xhtml.form.init({"class" : "news-edit",
                         "action" : "news-edit-action.cgi",
                         "method" : "post"})

  print xhtml.div.init()
  print xhtml.input.hidden({"name" : "message-id", "value" : news_item["message-id"]}),
  print xhtml.input.hidden({"name" : "from",       "value" : news_item["from"]}),
  print xhtml.input.hidden({"name" : "queue",      "value" : this_queue}),
  print xhtml.input.hidden({"name" : "editor",     "value" : editor}),

  print xhtml.table.init({"cellpadding" : "1", "cellspacing" : "0"})

  print xhtml.table.row(xhtml.table.cell("From:", {"class" : "news-edit"})
                        + xhtml.table.cell(cgi.escape(news_item["from"]),
                                           {"class" : "news-edit", "id" : "from"}))

  print xhtml.table.row(xhtml.table.cell("Message-Id:", {"class" : "news-edit"})
                        + xhtml.table.cell(wgo_news.safe_text(news_item["message-id"]),
                                           {"class" : "news-edit", "id" : "message-id"}))

  print xhtml.table.row(xhtml.table.cell("Subject:", {"class" : "news-edit"})
                        + xhtml.table.cell(xhtml.input.text({"name"  : "subject",
                                                             "class" : "subject",
                                                             "value" : cgi.escape(news_item.props["subject"]) }),
                                           {"class" : "news-edit", "id" : "subject"}))
  print xhtml.table.row(xhtml.table.cell("Date:", { "class" : "news-edit" })
                        + xhtml.table.cell(xhtml.input.text({"name"  : "date",
                                                             "class" : "date",
                                                             "value" : news_item["date"] }),
                                           {"class" : "news-edit", "id" : "date"}))
  print xhtml.table.row(xhtml.table.cell("Image:", {"class" : "news-edit"})
                        + xhtml.table.cell(image_selector, {"class" : "news-edit", "id" : "image"}))

  print xhtml.table.row(xhtml.table.cell(xhtml.input.textarea(cgi.escape(news_item["body"]),
                                                              {"name"  : "body",
                                                               "class" : "body",
                                                               "cols"  : "80",
                                                               "rows"  : "20" }),
                                         {"colspan" : "2"}))

  print xhtml.table.row(xhtml.table.cell("&nbsp;"))
  print xhtml.table.row(xhtml.table.cell(xhtml.input.submit({"name"  : "action", "value" : "save", "class" : "submit-button"})
                                         + approve_disapprove
                                         + xhtml.input.submit({"name"  : "action", "value" : "delete", "class" : "submit-button"}), {"colspan" : "2"}))

  print xhtml.table.fini()
  print xhtml.div.fini()
  print xhtml.form.fini()

  print xhtml.div("", {"style" : "height: 4ex;"}) # why is this necessary???

  print news_item.as_news_item()

  return (1)


def main():
  print "Content-type: text/html"

  wgo_news.head_boilerplate()

  form = cgi.FieldStorage()

  if not (form.has_key("message-id") and form.has_key("queue")):
    print xhtml.div("ERROR", {"class" : "heading"})
    print xhtml.div("Improper Request", {"class" : "subtitle"})
    return (1)

  message_id = wgo_news.safe_pathname(form["message-id"].value)

  queue = form["queue"].value
  
  if queue == wgo_news.config.pending_queue:
    this_queue = wgo_news.config.pending_queue
    other_queue = wgo_news.config.current_queue
  elif queue == wgo_news.config.current_queue:
    this_queue = wgo_news.config.current_queue
    other_queue = wgo_news.config.pending_queue
  elif queue == wgo_news.config.archive_queue:
    this_queue = wgo_news.config.archive_queue
    other_queue = wgo_news.config.archive_queue
  else:
    wgo_news.error("Improper request")
    wgo_news.foot_boilerplate()
    return (1)

  m = wgo_news.news_from_file(this_queue + "/" + message_id)
  if m == None:
    m = wgo_news.news()
    m["message-id"] = message_id
    m["date"] = rfc822.formatdate(time.time())
    pass

  editor = ""
  if os.environ.has_key("REMOTE_USER"):
    editor = os.environ["REMOTE_USER"]
    pass
  
  html_news_edit(this_queue, other_queue, m, editor)
  
  if wgo_news.config.validator != 0:
    print xhtml.validate()
    pass
  
  wgo_news.foot_boilerplate()

  return (0)

sys.exit(main())
