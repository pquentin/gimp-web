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
#
import fcntl
import email
import errno
import getopt
import mimetypes
import os
import re
import rfc822
import sys
import time
import types
import cgi
import mailbox

sys.path.append('__LIBDIR__')

import xhtml
import wgo
import wgo_news

def main(argv):

  fpin = sys.stdin
    
  if len(argv) > 1:
    fpin = open(argv[1], "r")
    mbox = mailbox.PortableUnixMailbox(fpin, email.message_from_file)
  else:
    mbox = [ email.message_from_file(fpin) ]
    pass

  for m in mbox:
    n = wgo_news.news(m)

    if n["message-id"] != None and n["message-id"] != "":
      s = wgo_news.re_substr("News:[ \t]*(.+)", n["subject"])
      if s != None:
        n["subject"] = cgi.escape(s)
        n["body"] = cgi.escape(n["body"])

        directory = wgo_news.queue_canonical_path(wgo_news.config.pending_queue)
        os.system('mkdir -p ' + directory)
        
        filename = wgo_news.queue_message_path(wgo_news.config.pending_queue, n["message-id"])

        n.to_queue(wgo_news.config.pending_queue)
        
        try:
          os.chmod(filename, wgo_news.config.news_permission)
          #os.chown(filename, wgo_news.config.news_user_uid)
        except:
          pass
        pass
      pass
    pass
            
  return (0)

sys.exit(main(sys.argv))

    
