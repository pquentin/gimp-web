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

import sys
import cgi
import cgitb; cgitb.enable()

sys.path = ['${LIBDIR}'] + sys.path

import wgo
import xhtml
import changelog


def wgo_xslt(filename):

  return (0)

def wgo_xhtml(filename):
  cl = changelog.ChangeLog(filename)

  print "Content-type: text/html"
  print
  
  extended_css = "/style/extended.css"
  
  print xhtml.include('%s/includes/wgo-xhtml-init.xhtml' % (wgo.config.DocumentRoot_path))
  print xhtml.title("GIMP - ChangeLog")
  print '<base href="/" />'
  
  print xhtml.link({"rel" : "stylesheet", "href" : extended_css, "type" : "text/css", "media" : "screen"})
  print xhtml.link({"rel" : "alternate stylesheet", "href" : "/about/ChangeLogs/changelog-xhtml.css", "type" : "text/css", "media" : "screen"})
  print xhtml.link({"rel" : "stylesheet", "href" : "/about/ChangeLogs/changelog-xhtml-mono.css", "type" : "text/css", "media" : "screen", "title" : "monospaced"})


  print xhtml.include('%s/includes/wgo-look-feel.xhtml' % (wgo.config.DocumentRoot_path))
  print xhtml.include('%s/includes/wgo-page-init.xhtml' % (wgo.config.DocumentRoot_path))
  
  print xhtml.div.init({"class" : "changelog"})
  for l in cl.logs:
    print xhtml.div(xhtml.span(xhtml.quote(l.date),     {"class" : "date"})
                    + xhtml.span(xhtml.quote(l.who),    {"class" : "author"})
                    + xhtml.span(xhtml.mailto(l.email), {"class" : "email"}), {"class" : "changelog-log"})
    
    print xhtml.list.init()
    for entry in l.body:
      print xhtml.list.item.init()
      paragraphs = entry.split("\n")
      format = xhtml.text
      for paragraph in paragraphs:
        print format(xhtml.quote(paragraph))
        format = xhtml.para
        pass

      print xhtml.list.item.fini()
      pass
    
    print xhtml.list.fini()
    pass

  print xhtml.div.fini()

  print xhtml.include('%s/includes/wgo-page-fini.xhtml' % (wgo.config.DocumentRoot_path))
  print xhtml.include('%s/includes/wgo-xhtml-fini.xhtml' % (wgo.config.DocumentRoot_path))
  
  return (0)


if __name__ == '__main__':

  if len(sys.argv) > 1:
    format = sys.argv[1]
  else:
    format = "xhtml"
    pass

  if len(sys.argv) > 2:
    input = sys.argv[2]
  else:
    input = "/home/wgo/about/ChangeLogs/1.2.3/ChangeLog"

  if format == "xhtml":
    sys.exit(wgo_xhtml(input))
  elif format == "rss":
    sys.exit(wgo_rss(input))
  elif format == "xslt":
    sys.exit(wgo_xslt(input))
  else:
    pass

  sys.exit(-1)
