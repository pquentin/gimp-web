#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-
#
import fcntl
import email
import errno
import getopt
import mimetypes
import os
import re
import rfc822
import sha
import sys
import time
import types
import cgi
import mailbox

sys.path.append('__LIBDIR__')

import xhtml
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

        directory = wgo_news.config.news_root + "/" + wgo_news.config.pending_queue
        
        os.system('mkdir -p ' + directory)
        filename = directory + "/" + n["message-id"]

        fp = open(filename, "w")
        print >>fp, n
        fp.close()
            
        try:
          os.chmod(filename, wgo_news.config.news_permission)
          os.chown(filename, wgo_news.config.news_user_uid)
        except:
          pass
        pass
      pass
    pass
        
            
  return (0)


sys.exit(main(sys.argv))

    
