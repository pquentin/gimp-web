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
import getopt
import sre as re
import string

sys.path = ['${LIBDIR}'] + sys.path # add the WGO CGI library directory to the Python import path

import wgo
import wgo_develop
import xhtml
import changelog
import rdf

  
def changelog_as_text(input, nlogs, title=""):

  changelog_entries = changelog.ChangeLog(input)

  for log in changelog_entries.logs[0:nlogs]:
    print log
    pass

  return (0)

# Given some text, look for things that look like references to bug
# numbers in bugzilla.  For each apparent reference, substitute a
# hyperlink to the bug in bugzilla.
#
def xhtml_interpolate_bug(text):
  
  bug_reference = "[Bb][Uu][Gg]\s*#([0-9]+)"

  s = ""
  last = 0
  
  for bug in re.finditer(bug_reference, text):
    s += text[last:bug.start()]
    s += str(xhtml.hyperlink("Bug #" + bug.expand("\\1"), {"href" : "http://bugzilla.gnome.org/show_bug.cgi?id=" + bug.expand("\\1")}))
    last = bug.end()
    pass

  s += text[last:]

  return (s)
  

# Format NLOGS worth of log entries from the ChangeLog file INPUT as xhtml
#
def changelog_as_xhtml(input, nlogs, title=""):
  wgo_develop.header("GIMP - ChangeLog",
                     [{"rel" : "stylesheet", "href" : "/about/ChangeLogs/changelog-xhtml.css", "type" : "text/css", "media" : "screen"}])

  print xhtml.div(title, {"class" : "heading"})
  # print xhtml.h1(title, {"class" : "heading"})
  
  print xhtml.div.init({"class" : "changelog"})

  changelog_entries = changelog.ChangeLog(input)

  for log in changelog_entries.logs[0:nlogs]:
    print xhtml.div(xhtml.span(xhtml.quote(log.date),     {"class" : "date"})
                    + xhtml.span(xhtml.quote(log.who),    {"class" : "author"})
                    + xhtml.span("<" + xhtml.mailto(log.email) + ">", {"class" : "email"}), {"class" : "changelog-log"})
    
    print xhtml.list.init()
    
    for entry in log.body:
      print xhtml.list.item.init()
      paragraphs = entry.split("\n")

      format = xhtml.text               # initially format without a <p></p> pair
      for paragraph in paragraphs:
        print format(xhtml_interpolate_bug(xhtml.quote(paragraph)))
        format = xhtml.para             # (any) subsequent paragraphs are enclosed in a <p></p> pair
        pass

      print xhtml.list.item.fini()
      pass
    
    print xhtml.list.fini()
    pass

  print xhtml.div.fini()

  wgo_develop.footer()
  
  return (0)

def changelog_as_rdf(input, nlogs, title=""):

  print xhtml.xml()

  print rdf.RDF.init()

  changelog_entries = changelog.ChangeLog(input)

  for log in changelog_entries.logs[0:nlogs]:
    print rdf.item(rdf.description(string.join(log.body)))
    print rdf.dc_creator(log.who)
    print rdf.dc_date(log.date)
    pass


  print rdf.RDF.fini()

  return (0)

def usage(name):
  print "Usage:", name, "[OPTION] [FILE]..."
  print "Print ChangeLog information in FILE in a particular output format."
  print
  print "  -h, --help                Print this message"
  print "  -f, --format=<format>     Output in <format> (xhtml, text, rss)"
  print "  -n, --nlogs=<number>      Print <number> of log entries and exit"
  print "  -t, --title=<string>      Print <string> as the top heading element content"
  print "  -v                        Print version and exit"
  return

if __name__ == '__main__':

  # By default, the output format is xhtml and the number of output
  # log entries is 10.
  
  output_format = "xhtml"
  nlogs = 10
  title = ""
  
  try:
    options, args = getopt.getopt(sys.argv[1:], "hf:n:vt:", ["help", "format=", "nlogs=", "version", "title="])
  except getopt.GetoptError:
    usage(sys.argv[0])
    sys.exit(2)
    pass

  for option, value in options:
    if option in ("-h", "--help"):
      usage(sys.argv[0])
      sys.exit(0)
    elif option in ("-f", "--format"):
      output_format = value
    elif option in ("-n", "--nlogs"):
      nlogs = int(value)
    elif option in ("-t", "--title"):
      title = value
    elif option in ("-v", "--version"):
      print Version
      sys.exit(0)
      pass
    pass

  for input in args:
    if output_format == "xhtml":
      sys.exit(changelog_as_xhtml(input, nlogs, title))
    elif output_format == "text":
      sys.exit(changelog_as_text(input, nlogs, title))
    elif output_format == "rss" or output_format == "rdf":
      sys.exit(changelog_as_rdf(input, nlogs, title))
    else:
      print >>sys.stderr, output_format, "is an unsupported output format."
      pass
    pass

  sys.exit(-1)
