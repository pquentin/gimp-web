#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
#
# www.gimp.org website administration and tools
#
# Copyright (C) 2002, 2003 Helvetix Victorinox, a pseudonym,
# Mountain View, California
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

import fcntl
import errno
import os
import re
import stat
import sys
import types
import cgi
import cgitb; cgitb.enable()

sys.path = ['${LIBDIR}'] + sys.path

import xhtml
import wgo
import wgo_news
import wgo_queue
    
def html_index_page(queue, news):
  if news == None or not news.valid:
    return (1)

  message_id = news["message-id"]

  filename = wgo_queue.message_path(queue, message_id)
  
  edit_target = "news-edit.cgi?message-id=" + xhtml.quote(message_id) + "&amp;queue=" + xhtml.quote(queue)

  checkbox_attrs = { "class" : "news-index", "name" : xhtml.quote(news["message-id"]) }
  if len(news["body"]) < 2:
    checkbox_attrs.update({"disabled" : "disabled"})
    pass
           
  attrs = { "class" : "news-index" }

  print xhtml.table.row(
    xhtml.table.cell(xhtml.quote(news["date"]), attrs)
    + xhtml.table.cell(xhtml.mailto(news["from"]), attrs)
    + xhtml.table.cell(xhtml.hyperlink(news["subject"], {"href" : edit_target, "class" : "news-index"}), attrs)
    + xhtml.table.cell(xhtml.input.checkbox(checkbox_attrs), attrs), attrs)
    
  return (1)

def main(queue):
  wgo_news.header()

  if queue in [wgo_news.config.pending_queue, wgo_news.config.current_queue, wgo_news.config.archive_queue]:
    dirpath = wgo.config.spool_path + queue
    names = map(lambda t: dirpath + "/" + t, os.listdir(dirpath))
    names.sort(lambda a, b: cmp(os.stat(a)[stat.ST_MTIME], os.stat(b)[stat.ST_MTIME]))

    #news = map(wgo_news.news, names)
    news = map(lambda f: wgo_news.news(f, False), names)
    news = filter(lambda n: n.valid, news)

    print xhtml.include('%s%s_header.html' % (wgo_news.config.news_path, queue))

    # If this is the pending queue, then create one initialised news article for display.
    if queue == wgo_news.config.pending_queue:
      html_index_page(queue, wgo_news.news())
      pass

    map(lambda n: html_index_page(queue, n), news)
                
    print xhtml.include('%s/%s_footer.html' % (wgo_news.config.news_path, queue))
    print xhtml.include(wgo_queue.generate_blotter(queue))
  else:
    print wgo.error("Malformed Request")
    pass
  
  wgo_news.footer()
  
  return (0)


if len(sys.argv) != 2:
  sys.exit(main(wgo_news.config.pending_queue))
  pass
    
sys.exit(main(sys.argv[1]))
