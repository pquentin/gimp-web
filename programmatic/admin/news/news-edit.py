#!/usr/bin/env ${PYTHON}
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

sys.path.append('${LIBDIR}')

import xhtml
import wgo
import wgo_news
import wgo_queue

# some sanity checking ought to be done to limit message sizes.
def html_news_edit(this_queue, other_queue, msg, editor):
  
  if this_queue == wgo_news.config.pending_queue and other_queue == wgo_news.config.current_queue:
    approve_disapprove = xhtml.input.submit({"name" : "action", "value" : "approve"})
    pass
  elif this_queue == wgo_news.config.current_queue and other_queue == wgo_news.config.pending_queue:
    approve_disapprove = xhtml.input.submit({"name" : "action", "value" : "disapprove"})
    pass
  else:
    approve_disapprove = ""
    pass

  image_selector = xhtml.input.select(wgo_news.icon_option_list(msg["image"]), { "name" : "image", "class" : "news-edit"})

  print xhtml.div("GIMP ORG News Administration :: Edit %s Item" % (string.capitalize(this_queue)), {"class" : "heading"})

  print xhtml.form.init({"class" : "news-edit", "action" : "news-edit-action.cgi", "method" : "post"})

  print xhtml.div.init()
  print xhtml.input.hidden({"name" : "message-id", "value" : xhtml.quote(msg["message-id"])})
  print xhtml.input.hidden({"name" : "from",       "value" : xhtml.quote(msg["from"])})
  print xhtml.input.hidden({"name" : "queue",      "value" : xhtml.quote(this_queue)})
  print xhtml.input.hidden({"name" : "editor",     "value" : xhtml.quote(editor)})

  print xhtml.table.init({"class" : "news-edit", "cellpadding" : "1"})

  print xhtml.table.row(xhtml.table.cell("From:") + xhtml.table.cell(xhtml.quote(msg["from"]), {"id" : "from"}))

  print xhtml.table.row(xhtml.table.cell("Message-Id:") + xhtml.table.cell(xhtml.quote(msg["message-id"]), {"id" : "message-id"}))

  print xhtml.table.row(xhtml.table.cell("Subject:") + xhtml.table.cell(xhtml.input.text({"name" : "subject", "value" : msg["subject"]}), {"id" : "subject"}))
  
  print xhtml.table.row(xhtml.table.cell("Date:") + xhtml.table.cell(xhtml.input.text({"name" : "date", "value" : msg["date"] }), {"id" : "date"}))

  print xhtml.table.row(xhtml.table.cell("Image:") + xhtml.table.cell(image_selector, {"id" : "image"}))
  
  print xhtml.table.row(xhtml.table.cell("Editor:") + xhtml.table.cell("wilber", {"id" : "editor"}))
  
  print xhtml.table.row(xhtml.table.cell(xhtml.input.textarea(msg["body"], {"name"  : "body", "cols" : 80, "rows"  : 20 }), {"colspan" : "2"}))
  
  print xhtml.table.row(xhtml.table.cell("&nbsp;"))
  
  print xhtml.table.row(xhtml.table.cell(xhtml.input.submit({"name" : "action", "value" : "save"})
                                         + approve_disapprove
                                         + xhtml.input.submit({"name" : "action", "value" : "delete"}),
                                         {"colspan" : "2"}))
  
  print xhtml.table.fini()
  print xhtml.div.fini()
  print xhtml.form.fini()

  print xhtml.div("&nbsp;")

  print msg.as_news_item()

  return (1)


def main():
  wgo_news.header()

  form = cgi.FieldStorage()

  if not (form.has_key("message-id") and form.has_key("queue")):
    wgo_news.footer(wgo.error("Malformed Request"))
    return (1)

  queue = form["queue"].value
  
  if queue in ["pending", wgo_news.config.pending_queue]:
    this_queue = wgo_news.config.pending_queue
    other_queue = wgo_news.config.current_queue
  elif queue in ["current", wgo_news.config.current_queue]:
    this_queue = wgo_news.config.current_queue
    other_queue = wgo_news.config.pending_queue
  elif queue in ["archive", wgo_news.config.archive_queue]:
    this_queue = wgo_news.config.archive_queue
    other_queue = wgo_news.config.archive_queue
  else:
    wgo_news.footer(wgo.error("Malformed request"))
    return (1)

  message_id = xhtml.unescape(form["message-id"].value)

  try:
    m = wgo_news.news(wgo_queue.message_path(this_queue, message_id))
  except:
    m = wgo_news.news()
    m["message-id"] = message_id
    m["date"] = rfc822.formatdate(time.time())
    pass

  if os.environ.has_key("REMOTE_USER"):
    editor = os.environ["REMOTE_USER"]
  else:
    editor = "wilber@gimp.org"
    pass
  
  html_news_edit(this_queue, other_queue, m, editor)
  
  wgo_news.footer()
  
  return (0)

sys.exit(main())
