#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-

import fcntl
import email
import errno
import getopt
import mimetypes
import os
import re
import rfc822
import stat
import sys
import time
import types
import Cookie
import cgi
import mailbox
#import cgitb; cgitb.enable()

sys.path.append('__LIBDIR__')

import xhtml
import wgo_news

    
def html_index_page(queue, news):
  if news == None:
    return (1)

  message_id = wgo_news.safe_pathname(news["message-id"])

  subject = cgi.escape(news["subject"])

  target = "news-edit.cgi?message-id=" + message_id + "&amp;queue=" + queue
  filename = queue + "/" + message_id
  
  checkbox_attrs = { "class" : "news-index", "name" : filename }
  if len(news["body"]) < 2:
    checkbox_attrs = { "class" : "news-index", "disabled" : "disabled", "name" : filename }
    pass
           
  attrs = { "class" : "news-index" }

  print xhtml.table.row(
    xhtml.table.cell(cgi.escape(news["date"]), attrs)
    + xhtml.table.cell(xhtml.mailto(cgi.escape(news["from"])), attrs)
    + xhtml.table.cell(xhtml.hyperlink(subject, {"href" : target, "class" : "news-index"}), attrs)
    + xhtml.table.cell(xhtml.input.checkbox(checkbox_attrs), attrs),
    attrs)
    
  return (1)

def main(argv):
  print "Content-type: text/html"
  
  wgo_news.head_boilerplate()

  queue = argv[1]
    
  if queue == wgo_news.config.pending_queue or queue == wgo_news.config.current_queue or queue == wgo_news.config.archive_queue:
            
    print xhtml.include('%s/include/%s_header.inc' % (wgo_news.config.news_root, queue))

    # Create one initialised news article in the pending queue
    if queue == wgo_news.config.pending_queue:
      html_index_page(queue, wgo_news.news())
      pass

    names = map(lambda t: queue + "/" + t, os.listdir(queue))
    names.sort(lambda a, b: cmp(os.stat(a)[stat.ST_MTIME], os.stat(b)[stat.ST_MTIME]))

    news = map(wgo_news.news_from_file, names)
    map(lambda n: html_index_page(queue, n), news)
                
    print xhtml.include('%s/include/%s_footer.inc' % (wgo_news.config.news_root, queue))
    
    wgo_news.news_generate_blotter(queue)
    
    try:
      print xhtml.include(queue + "/" + wgo_news.config.news_blotter)
    except:
      pass
    pass
  else:
    wgo_news.error("Malformed Request")
    pass
  
  if wgo_news.config.validator != 0:
    print xhtml.validate()
    print xhtml.environ()
    pass
  
  wgo_news.foot_boilerplate()
  
  return (0)


if len(sys.argv) != 2:
  print 'usage: news-index.cgi [current|pending|archive]'
  sys.exit(1)
  pass
    
sys.exit(main(sys.argv))
