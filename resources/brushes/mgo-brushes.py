#!/usr/bin/env python

import string
from gimpfu import *

def write_brush_page(bg_colour, fg_colour, page_location):
    f = open(page_location + 'index.html', 'w')
    f.write('<!--#include virtual="/includes/header_pretitle.inc" -->\n')
    f.write('<title>GIMP - Resources</title>\n')
    f.write('<!--#include virtual="/includes/header_posttitle.inc" -->\n')
    f.write('<!--#include virtual="/includes/menu.inc" -->\n')
    f.write('<!--This page rendered with mgo-brushes -->\n')
    f.write('<div class="heading">Resources</div>\n') 
    f.write('<div class="subtitle">Included With The GIMP</div>\n') 
    f.write('<p>More than just a bunch of tools, The GIMP has stuff too ....</p>\n') 
    f.write('<div>this is the beginning</div>\n') 
    num_brushes, brushlist = pdb.gimp_brushes_list()
    old_fg = gimp.get_foreground()
    old_bg = gimp.get_background()
    half = int(round(num_brushes / 2.0))
    count = 0
    for a in brushlist:
        pdb.gimp_brushes_set_brush(a)
        name, width, height, spacing = pdb.gimp_brushes_get_brush()
        count += 1
        rmspace = string.maketrans(" ","_")
        pname = string.translate(name, rmspace,'()#,')
        image = pdb.gimp_image_new(width + 31, height + 31, RGB)
        drawable = gimp.layer(image, a, width + 30, height + 30, RGBA_IMAGE, 100, 0)
        image.add_layer(drawable, 0)
        gimp.set_foreground(fg_colour)
        gimp.set_background(bg_colour)
        pdb.gimp_edit_fill(drawable, BG_IMAGE_FILL)
        iwidth = width + 31
        center = iwidth/2.0
        num_strokes = 2
        new_width = 32
        new_height = 32
        pdb.gimp_paintbrush_default(drawable, num_strokes, [center, center])
        pdb.gimp_image_scale(image, new_width, new_height)
        pdb.gimp_file_save(image, drawable, page_location + pname + '.png', pname + '.png')
        pdb.gimp_image_delete(image)
        f.write('<div><img src="' + pname + '.png" width="32" height="32" alt="brush sample"><p>' + name + '</p></div>\n')
        if count == half:
            f.write('<div><p>half way point</p></div>\n') 
    f.write('\n') 
    f.write('<!--#include virtual="/includes/linkbar.inc" -->\n') 
    f.write('<!--#include virtual="/includes/footer.inc" -->\n') 
    f.close()
    gimp.set_background(old_bg)
    gimp.set_foreground(old_fg)
register(
	"python_fu_mgo_brushes_xhtml",
	"Writes a resource web page and generates the sample images",
	"Writes a resource web page and generates the sample images",
	"Carol Spears",
	"Carol Spears",
	"2002",
	"<Toolbox>/Xtns/Python-Fu/mgo/brush",
	"RGB*, GRAY*",
	[
		(PF_COLOR, "bg_colour", "background", (255,255,255)),
		(PF_COLOR, "fg_colour", "foreground", (0,0,0)),
        (PF_FILE, "page_location", "page_location", "wgo/resources/brushes/")
	],
	[],
	write_brush_page)

main()
