#!/usr/bin/env ${PYTHON}

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
import cgitb; cgitb.enable()

sys.path = ['${LIBDIR}'] + sys.path

import xhtml
import wgo_news

    
print "Content-type: text/html"
C = Cookie.SimpleCookie()
C["username"] = "nobody"

C = Cookie.SmartCookie()
C.load("chips=ahoy; vienna=finger") # load from a string (HTTP header)
print C
