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

# A Python programmatic interface to a ChangeLog.
#
# See accompanying Python scripts for examples of how I use this.
#
# I wish I could find (or that it would exist) a definitive
# description of a ChangeLog format.  In lieu of this, I am using
# ChangeLogs produced and understood by Lord Emacs, Keeper of the True
# Faith and Harbinger of all things Gnu.

import rfc822
import types
import string
import sys
import os
import re
import pprint

pp = pprint.PrettyPrinter(indent=2)

#
#
# The start of a log entry varies but conforms abstractly to:
#
#        timestamp name email
# 
# A log has a list of paragraphs for which each paragraph may have sub-paragraphs
#
#        * gimp-zip.in: Include minizip.exe (for the gz plug-in) (bug# 67135).     <- Paragraph
#        Put gif plug-in in a separate zipfile.
#
#        * libgimp/gimpenv.c (gimp_directory): (Win32) When no home                <- Paragraph
#          directory has been found, and we use a user-specific directory in
#          the GIMP installation directory: If the user name contains
#          characters that are illegal in file (or folder) names, replace
#          those characters with underscores (bug# 64491).
#
#          Actually also some legal, but odd, characters get replaced.              <- Sub-paragraph
#          Hmm. There are problems here related to i18n. In multi-byte
#          locales g_get_user_name() presumably, at least currently, returns
#          a multi-byte string encoded in some Windows multi-byte code page,
#          and the code here will think that some or most characters in it
#          are "odd", and replace them with underscores. This will cause
#          different user names in Japanese, for instance, that happen to
#          have the same length, to be convered to the same string of
#          underscores.)
#


class Log:
  def __init__(self, date, who, email, log):
    self.date = str(date)
    self.who = str(who)
    self.email = str(email)
    self.body = []

    for x in log.split("\n*"):
      if len(x) > 1 and x[0] == '*': x = x[1:]
      x = x.strip()
      x = x.replace("\n\n", "\001\001")
      x = x.replace("\n", " ")
      x = x.replace("\001\001", "\n")
      self.body.append(x)
      pass
    
    return (None)

  def __getitem__(self, name):
    print "__getitem__:", name
    return (None)
  
  def fmt(self, s, max=60, prefix=""):
    new = ""

    for l in s.split("\n"):
      while len(l) > 0:
        if len(l) > max:
          idx = max
          while idx > 0 and l[idx] not in string.whitespace: idx = idx - 1
          if idx == 0:
            new = l
            break
          new += prefix + l[:idx] + "\n"
          l = (l[idx:]).strip()
        else:
          new += prefix + l
          break
        pass
      new += "\n\n"
      pass
  
    return (new.strip())

  def __repr__(self):
    date = self.date
    email = self.email
    
    if date == None: date = "unknown date"
    if email == None: email = ""
    s = date + "\t" + self.who + "\t" + email + "\n\n"

    for entry in self.body:
      entry = "* " + entry
      paragraphs = entry.split("\n")
      
      for line in paragraphs:
        l = self.fmt(line, 60, "\t")
        s = s + "\t" + l + "\n\n"
        pass
      pass

    s += "\n"

    return (s)

  pass

class ChangeLog:
  def __init__(self, input=None):
    self.logs = []
    if input != None:
      if str(input.__class__) == "<type 'str'>":
        fp = open(input, "r")
        pass

      lines = fp.readlines()

      while len(lines) > 0:
        lines = self.parse(lines)
        pass
      
      pass

    return (None)

  def __repr__(self):
    s = ""
    for l in self.logs:
      s += l.__repr__()
      pass

    return (s)
    

  def parse(self, lines):
    idx = 0
    done = False
    while not done:
      if len(lines[idx]) > 0 and lines[idx][0] not in string.whitespace:
        done = True
        pass
      pass
    
    header = lines[idx]
    idx = idx + 1
    
    date = None

    if date == None:
      match = re.match("^(\d+)-(\d+)-(\d+)", header)
      if match != None:
        date = match.expand("\\1-\\2-\\3")
        header = header.replace(date, "")
        pass
      pass
    
    if date == None:
      match = re.match(r"^([A-Z][a-z]{2}\s[A-Z][a-z]{2}\s+\d+\s+\d+:\d+:\d+\s.+\d{4})", header)
      if match != None:
        date = match.expand("\\1")
        header = header.replace(date, "")
        pass
      pass
    
    email = None
    match = re.search("(<[^>]+>)", header)
    if match != None:
      email = match.expand("\\1")
      header = header.replace(email, "")
      pass
    
    if email != None: header = header.replace(email, "")
    if date != None: header = header.replace(date, "")
    
    who = header.strip()
    
    # Skip the blank lines between the header and the message itself
    while lines[idx] == "\n":
      idx = idx + 1
      pass

    body = ""
    
    line = lines[idx]
    while line[0] in string.whitespace:
      body += line.strip() + "\n"
      idx = idx + 1
      if idx > len(lines) - 1: break
      line = lines[idx]
      pass
    
    self.logs.append(Log(date, who, email, body))
    return (lines[idx:])

  pass


if __name__ == '__main__':
  cl = ChangeLog(sys.argv[1])
  print cl
