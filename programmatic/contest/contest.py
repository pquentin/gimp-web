#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
# "every tool is a weapon, if you hold it right."
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

import fcntl
import errno
import getopt
import os
import stat
import sys
import time
import types
import cgi
import cgitb; cgitb.enable()

sys.path = ['${LIBDIR}'] + sys.path

import xhtml
import wgo
import wgo_contest

def tempfile(path="", prefix="", suffix=""):
  filename = path + prefix + str(time.strftime("%Y%m%d%H%M%S", time.gmtime())) + str(os.getpid()) + suffix
  return (filename)


def submit_manually(args):
  try:
    opts, args = getopt.getopt(sys.argv[1:], "ha:t:e:", ["help", "author=", "title=", "email="])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
    pass
  
  title = ""
  email = ""
  author = ""
  
  for o, a in opts:
    if o in ("-h", "--help"):
      print "-a, --author: author name"
      print "-e, --email: email name"
      print "-t, --title: title name"
      sys.exit()
      pass
    if o in ("-a", "--author"): author = a
    if o in ("-e", "--email"): email = a
    if o in ("-t", "--title"): title = a
    pass

  for arg in args:
    name = tempfile("")
    entry = wgo_contest.gallery_image(name)

    try:
      os.system("/usr/X11R6/bin/convert '%s' 'png:%s'" % (arg, wgo.config.DocumentRoot_path + entry["image"]))
      os.system("/usr/X11R6/bin/convert -geometry 150 '%s' 'png:%s'\n" % (wgo.config.DocumentRoot_path + entry["image"],
                                                                          wgo.config.DocumentRoot_path + entry["thumb"]))
      os.system("/usr/X11R6/bin/convert -geometry 150 '%s' 'jpg:%s'\n" % (wgo.config.DocumentRoot_path + entry["image"],
                                                                          wgo.config.DocumentRoot_path + entry["thumb"]))
      #os.chown(wgo.config.DocumentRoot_path + entry["image"], wgo.config.user_uid, wgo.config.user_gid)
      #os.chown(wgo.config.DocumentRoot_path + entry["thumb"], wgo.config.user_uid, wgo.config.user_gid)
    except Exception, e:
      print arg, name, e
      return (False)

    entry["title"] = title
    entry["author"] = author
    entry["email"] = email
    entry.save()

    if not entry.exists():
      print "Eeek! Gallery became insane. Failed to add entry: ", name
      return (-1)
  
    print name, "success"
    pass

  return (0)


def submit(form):
  wgo_contest.folio_init("GIMP Splash Image Contest Submission")
  
  image = 'images/gimp-splash.png'
  author = "Wilber Gimp"
  email = "wilber@gimp.org"

  print xhtml.h1("GIMP Splash Image Contest", {"class" : "heading"})
  #xhtml.div(thumb, {"class": "splash-thumb", "style" : "float: right; margin-left: 1em;"})
  print xhtml.para("""Welcome to the www.gimp.org splash image contest.
  From here you may submit images to be considered as candidates
  for a "splash" image.  We appreciate your participation, but there are
  No Promises on what may become of your image here.""")

  print xhtml.h2("Submit Your Image", {"class" : "subtitle"})

  cell = xhtml.table.cell
  row = xhtml.table.row

  thumb = wgo_contest.image_generate("Your Image Here", image, "Wilber", "wilber@gimp.org")

  fields = (xhtml.table.init({"cellspacing" : 0})
            + row(cell("File name:",     {"style" : "font-weight: bold"}) + cell(xhtml.input.file({"name" : "image"})))
            + row(cell("Title:",         {"style" : "font-weight: bold"}) + cell(xhtml.input.text({"name" : "title"})))
            + row(cell("Artist's Name:", {"style" : "font-weight: bold"}) + cell(xhtml.input.text({"name" : "author"})))
            + row(cell("Artists Email:", {"style" : "font-weight: bold"}) + cell(xhtml.input.text({"name" : "email"})))
            + row(cell(xhtml.input.hidden({"name" : "mode","value" : "preview"})) + cell(xhtml.input.submit({"name" : "preview", "value" : "PREVIEW"})))
            + xhtml.table.fini())
  
  form = xhtml.form(fields, {"enctype" : "multipart/form-data",
                             "method" : "post",
                             "action" : "contest.cgi",
                             "style" : "margin: 1.33em 0px; margin-left: 40px; margin-right: 40px;" })

  guidelines = (xhtml.para("""Past splash images range in approximate pixel widths and heights from 300x300 to 550x400 pixels. """
                           """Other sizes could be considered, if the artwork merits an unusual size.""")
                + xhtml.para("Fill in the fields below, and click the "
                             + xhtml.input.submit({"value" : "PREVIEW", "disabled" : "disabled"})
                             + " button below."))

  print guidelines
  print form

  wgo_contest.folio_fini()
  return


def preview(form):
  name = tempfile("")

  image_path = wgo_contest.spool_path(name, ".png")
  thumb_path = wgo_contest.spool_path(name, "-t.png")
  thumb_path = wgo_contest.spool_path(name, "-t.jpg")
  
  image_file = wgo_contest.spool_file(name, ".png")
  thumb_file = wgo_contest.spool_file(name, "-t.png")
  thumb_file = wgo_contest.spool_file(name, "-t.jpg")
  
  author = form.getvalue("author", "unknown")
  email = form.getvalue("email", "")
  title = form.getvalue("title", "")

  if len(form["image"].value) == 0:
    wgo_contest.folio_init("GIMP Splash Image Contest Preview Failed")
    print wgo.error("You didn't submit an image.")
    wgo_contest.folio_fini()
    return (1)

  execute_string = "convert - 'png:%s'" % (image_path)
  try:
    fp = os.popen("/usr/bin/convert - 'png:%s'" % (image_path), "w")
    fp.write(form["image"].value)
    fp.close()
    os.system("/usr/bin/convert -geometry 150 '%s' 'png:%s'\n" % (image_path, thumb_path))
    os.system("/usr/bin/convert -geometry 150 '%s' 'jpg:%s'\n" % (image_path, thumb_path))
  except Exception, e:
    wgo_contest.folio_init("GIMP Splash Image Contest Preview Failed")
    try: os.remove(image_path)
    except: pass
    try: os.remove(thumb_path)
    except: pass

    print wgo.error(str(e))
    wgo_contest.folio_fini()
    return (1)

  wgo_contest.folio_init("GIMP Splash Image Contest Preview")

  print xhtml.h1("GIMP Splash Image Contest", {"class" : "heading"})
  print xhtml.para("""Welcome to the www.gimp.org splash image contest. """
                   """From here you may submit images to be considered as candidates
                   for a "splash" image.  We appreciate your participation, but we
                   offer No Promises on what may become of your image here.""")

  print xhtml.h2("Approve Your Image", {"class" : "subtitle"})

  form = xhtml.form(xhtml.input.submit({"name" : "approve", "value" : "APPROVE"})
                    + xhtml.input.hidden({"name" : "mode", "value" : "approve"})
                    + xhtml.input.hidden({"name" : "name", "value" : name})
                    + xhtml.input.hidden({"name" : "title", "value" : title})
                    + xhtml.input.hidden({"name" : "author", "value" : author})
                    + xhtml.input.hidden({"name" : "email", "value" : email}),
                    {"enctype" : "multipart/form-data", "method" : "post", "action" : "contest.cgi"})

  thumb = wgo_contest.image_generate(title, thumb_file, author, email)
    
  img = wgo_contest.image_generate(title, image_file, author, email)

  guidelines = (xhtml.para(xhtml.span(xhtml.div(thumb, {"class": "splash-thumb"}), {"style" : "float: right; margin-left: 1em;"})
                           + """Below is your image as we see it, in its original size surrounded
                           by a red border 2 pixels thick over a background of alternating
                           light and dark grey squares to make the transparency and size
                           of the image clear. """
                           """To the right is a thumbnail image 150 pixels wide and proportionate height.""",
                           { "style" : "text-align: justify;"})
                + xhtml.para("""If this is the image you want to submit, click on the """
                             + xhtml.input.submit({"value" : "APPROVE", "disabled" : "disabled"})
                             + """ button below. """
                             """Otherwise, use your browser's Back button to submit another image.""", {"style" : "text-align: justify;"})
                + xhtml.para("""If you do not see your image, there are a large number of potential reasons. """
                             """Verify the name of the file that you are trying to submit. """
                             """Ensure that the file you are submitting is an image. """
                             """We may have run out of temporary space on our server. """
                             """Do not submit animated images, or images with more than one scene. """
                             """If the failure persists, please send a message to the webmaster""")
                + xhtml.para("""Nota Bene: You have %d minutes to approve this image."""
                             """After that time, you will need to resubmit your image.""" % (wgo_contest.config.tmp_directory_ttl)))

  print guidelines
  print xhtml.div(img, {"class" : "splash-image", "id" : "preview"})
  print form

  wgo_contest.folio_fini()
  return


def approved(form):
  wgo_contest.folio_init("GIMP Splash Image Contest Submission Approved")

  print xhtml.h1("GIMP Splash Image Contest", {"class" : "heading"})
  print xhtml.para("""Welcome to the www.gimp.org splash image contest. """
                   """From here you may submit images to be considered as candidates for a "splash" image.""")
  print xhtml.h2("Thank You!", {"class" : "subtitle"})
  print xhtml.para("Again, we offer No Promises on what may become of your image here.")
  
  name = os.path.basename(form.getvalue("name", ""))
  entry = wgo_contest.gallery_image(name)
  entry["title"] = xhtml.quote(form.getvalue("title", ""))
  entry["author"] = xhtml.quote(form.getvalue("author", ""))
  entry["email"] = xhtml.quote(form.getvalue("email", ""))

  image_path = wgo_contest.spool_path(name, ".png")
  thumb_path = wgo_contest.spool_path(name, "-t.png")
  thumb_path = wgo_contest.spool_path(name, "-t.jpg")
  
  image_file = wgo_contest.gallery_file(name, ".png")
  thumb_file = wgo_contest.gallery_file(name, "-t.png")
  thumb_file = wgo_contest.gallery_file(name, "-t.jpg")
  image_html = wgo_contest.gallery_path(name, ".html")
  thumb_html = wgo_contest.gallery_path(name, "-t.html")
  
  os.system("/bin/cp -f '%s' '%s' '%s'" % (image_path, thumb_path, wgo_contest.config.gallery_path))

  entry.save()

  #print xhtml.div(entry.ashtml("image"), {"class" : "splash-image"})
  print entry.ashtml("image")

  print xhtml.para("You can " + xhtml.hyperlink("submit another image", {"href" : "/contest/contest.cgi"})
                  + " or "  + xhtml.hyperlink("view the gallery.", {"href" : "/contest/gallery.cgi?display=gallery"}))

  wgo_contest.folio_fini()
  return
  

def main(argv):
  form = cgi.FieldStorage()

  if os.environ.has_key("GATEWAY_INTERFACE"):
    mode = form.getvalue("mode", "form")
  else:
    mode = "manual"
    pass

  if mode == "manual":          sys.exit(submit_manually(argv[1:]))
  elif mode == "form":          submit(form)
  elif mode == "preview":       preview(form)
  elif form.has_key("approve"): approved(form)
  else:
    pass
  
  return (0)

sys.exit(main(sys.argv))
