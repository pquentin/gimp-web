#!/usr/bin/env python
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

import email
import email.MIMEMessage
import cgi
import errno
import fcntl
import getopt
import xhtml
import mimetypes
import os
import re
import rfc822
import stat
import string
import sys
import time
import types

import wgo

def head_boilerplate(css=[], headers=[]):
  headers = headers + ["Content-type: text/html"]
  for h in headers: print h
  
  css = css + [wgo.config.admin_dir + "wgo-admin.css"]
  
  return (wgo.header("www.gimp.org - Administration", css, wgo.config.DocumentRoot_path + '/includes/admin-menu.inc'))

def footer():
  return (wgo.footer())