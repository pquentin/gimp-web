#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-

import email
import errno
import fcntl
import getopt
import xhtml
import mimetypes
import os
import re
import rfc822
import sha
import stat
import string
import sys
import time
import types

import config

def safe_pathname(path):
  path = string.replace(path, "/", "")
  return (path)

def safe_text(s):
  s = string.replace(s, "&", "&amp;")
  s = string.replace(s, "<", "&lt;")
  s = string.replace(s, ">", "&gt;")
  s = string.replace(s, '"', "&quot;")
  
  return (s)

#
def re_substr(regex, str):
  if str != None:
    regex = re.compile(regex).search(str, 0)
    if regex != None:
      return regex.expand("\\1")
    pass
    
  return None

class news:
  def __init__(self, email=None):
    self.props = { }
    self.props["date"] = "now"
    self.props["from"] = "wilber@news.gimp.org"
    self.props["reply-to"] = ""
    self.props["subject"] = "(none)"
    self.props["message-id"] = time.strftime("%Y%m%d%H%M%S-") + sha.new("%s" % (os.getpid())).hexdigest()[0:5] + "@news.gimp.org"
    self.props["body"] = ""
    self.props["image"] = "default.png"
    self.props["editor"] = ""

    if email != None:
      self.init_from_email(email)
      pass
            
    return (None)

    
  def init_from_email(self, msg):
    self.props["from"] = self.from_from_email(msg)
    self.props["subject"] = msg.get("subject")
    self.props["date"] = self.date_from_email(msg)
    self.props["message-id"] = self.message_id_from_email(msg)

    image = msg.get("x-gimp-org-image")
    if image == None:
      image = "default.png"
      pass

    self.props["image"] = image

    editor = msg.get("x-gimp-org-editor")
    if editor == None:
      editor = ""
      pass
    self.props["editor"] = editor

    if not msg.is_multipart():
      body = msg.get_payload()
      body = string.replace(body, "\n", "")
      body = string.replace(body, "\r", "")
    else:
      print "can't handle multipart messages"
      pass
        
    return (self)

  def __getitem__(self, name):
    return str(self.props[name])
    
  def __setitem__(self, name, value):
    self.props[name] = value
    return (self)

  def __repr__(self):
    s = "From " + str(self.props["from"]) + " " + time.strftime("%a, %b %d %Y %H:%M:%S +0000", rfc822.parsedate(self["date"])) + "\n"
    s += "From: <" + str(self.props["from"]) + ">\n"
    s += "Date: " + str(self.props["date"]) + "\n"
    s += "Subject: " + str(self.props["subject"]) + "\n"
    s += "Message-Id: <" + str(self.props["message-id"]) + ">\n"
    s += "X-Gimp-Org-Image: " + str(self.props["image"]) + "\n"
    s += "X-Gimp-Org-Editor: " + str(self.props["editor"]) + "\n"
    s += "\n"
    s += str(self.props["body"])
    return s
       
  def from_from_email(self, email_msg):
    from_ = re_substr(".*<(.+)@(.+)>.*", email_msg.get("reply-to"))
    if from_ == None:
      from_ = re_substr(".*<(.+@.+)>.*", email_msg.get("sender"))
      if from_ == None:
        from_ = re_substr(".*<(.+@.+)>.*", email_msg.get("from"))
        pass
      pass
        
    return (from_)


  def date_from_email(self, email_msg):
    try:
      date = email_msg.get("date")
      try:
        d = rfc822.formatdate(time.mktime(rfc822.parsedate(date)))
        return (d)
      except:
        pass
      return (date)
    except:
      pass
    return (None)

  def message_id_from_email(self, email_msg):
    message_id = re_substr(".*<(.+)>.*", email_msg.get("message-id"))
    if message_id == None:
      message_id = time.strftime("%Y%m%d%H%M%S-") + sha.new("%s" % (os.getpid())).hexdigest()[0:5] + "@news.gimp.org"
      pass
      
    # we don't ever allow any slashes or ampersands in the message-id
    message_id = string.replace(message_id, "/", "")
    message_id = string.replace(message_id, "&", "")
    return (message_id)

  def as_news_item(self):
    iso_date = time.strftime(config.datetime_format, rfc822.parsedate(self.props["date"]))

    subject = safe_text(self.props["subject"])
    
    s = '<div class="newsheading">'
    s += '<span class="newstitle">%s</span>' % (subject)
    s += '<span class="newsdate">%s</span>' % (iso_date)
    s += '&nbsp;</div>'
    s += '<p class="news">'
    s += '<img src="%s/%s" alt="" class="icon" />' % (config.news_icon_path, self.props["image"])
    s += self.props["body"]
    s += '</p>'

    return (s)
  
  pass
  
def news_from_email(e):
  m = news()
  m.props["from"] = m.from_from_email(e)
  m.props["subject"] = e.get("subject")
  m.props["date"] = m.date_from_email(e)
  m.props["message-id"] = m.message_id_from_email(e)

  image = e.get("x-gimp-org-image")
  if image == None:
    image = "default.png"
    pass
  m.props["image"] = image

  editor = e.get("x-gimp-org-editor")
  if editor == None:
    editor = ""
    pass
  
  m.props["editor"] = editor

  if not e.is_multipart():
    body = e.get_payload()
    body = string.replace(body, "\n", "")
    body = string.replace(body, "\r", "")
  else:
    return (None)

  m.props["body"] = body
  return (m)

    
def news_from_fd(fp):
  try:
    e = email.message_from_file(fp)
    m = news_from_email(e)
    return (m)
  except:
    pass
  return (None)

        
def news_from_file(filename):
  fd = open(filename, "r")
  m = news_from_fd(fd)
  fd.close()
  return (m)


def news_to_file(news, queue):
  fp = open(queue + "/" + news["message-id"], "w")
  print >>fp, news
  fp.close()
  return (0)

def news_from_form(form):
  #    try:
  n = news()
    
  if not form.has_key("message-id"):
    return (None)
    
  n["message-id"] = safe_pathname(form["message-id"].value)
  
  if form.has_key("date"):
    date = rfc822.parsedate(form["date"].value)
    date = time.mktime(date)
    date = rfc822.formatdate(date)
    n["date"] = date
  else:
    n["date"] = ""
    pass
    
  if form.has_key("from"):
    n["from"] = form["from"].value
  else:
    n["from"] = ""
    pass

  if form.has_key("subject"):
    n["subject"] = form["subject"].value
  else:
    n["subject"] = "New"
    pass
    
  if form.has_key("image"):
    n["image"] = form["image"].value
  else:
    n["image"] = "default"
    pass

  if form.has_key("body"):
    body = form["body"].value
  else:
    body = ""
    pass
  
  body = string.replace(body, "\n", "")
  body = string.replace(body, "\r", "")
  n["body"] = body
  
  return (n)
#    except:
#        pass

#return (None)
    

#
#
def news_generate_blotter(queue):
  names = map(lambda t: queue + "/" + t, os.listdir(queue))
  names.sort(lambda a, b: cmp(os.stat(a)[stat.ST_MTIME], os.stat(b)[stat.ST_MTIME]))
             
  news_blotter = queue + "/" + config.news_blotter
    
  fp_out = open(news_blotter, "w")
    
  print >>fp_out, "<!-- begin chartae -->"
  for n in names:
    if n != news_blotter:
      m = news_from_file(n)
      print >>fp_out, m.as_news_item()
      pass
    pass
      
  print >>fp_out, "<!-- end chartae -->"
            
  fp_out.close()

  try:
    os.chmod(news_blotter, 0666)
    os.chown(news_blotter, news_user_uid)
  except:
    pass

  return (0)

def head_boilerplate():
  print
  print xhtml.include('%s/includes/header_pretitle.inc' % (config.installdir))
  print xhtml.title('GIMP - The GNU Image Manipulation Program')
  print xhtml.link(None, { "href" : "/%s/news.css" % (config.news_directory)})
  print xhtml.include('%s/includes/header_posttitle.inc' % (config.installdir))

  print xhtml.include('%s/include/news_menu.inc' % (config.news_root))
  return

def foot_boilerplate():
  print xhtml.include('%s/includes/linkbar.inc' % (config.installdir))
  print xhtml.include('%s/includes/footer.inc' % (config.installdir))
  return

def error(msg):
  print xhtml.div("ERROR", {"class" : "heading"})
  print xhtml.div(msg, {"class" : "subtitle"})
  return (0)
