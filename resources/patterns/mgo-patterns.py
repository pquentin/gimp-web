#!/usr/bin/env python

import string
from gimpfu import *

def write_pattern_page(bg_colour, fg_colour, page_location):
    f = open(page_location + 'index.html', 'w')
    f.write('<!--#include virtual="/includes/header_pretitle.inc" -->\n')
    f.write('<title>GIMP - Resources - Patterns</title>\n')
    f.write('<!--#include virtual="/includes/header_posttitle.inc" -->\n')
    f.write('<!--#include virtual="/includes/menu.inc" -->')
    f.write('<!--This page rendered with mgo-patterns -->\n')
    f.write('<div class="heading">Resources - Patterns</div>\n') 
    f.write('<div class="subtitle">Included With The GIMP</div>\n') 
    f.write('<p>More than just a bunch of tools, The GIMP has stuff too ....</p>\n') 
    f.write('<div>this is the beginning</div>\n') 
    num_patterns, pattern_list = pdb.gimp_patterns_list()    
    old_pat, width, height = pdb.gimp_patterns_get_pattern()    
    half = int(round(num_patterns / 2.0))
    count = 0
    for a in pattern_list:
        pdb.gimp_patterns_set_pattern(a)
        count += 1
        name, width, height, mask_bpp, length, mask_data = pdb.gimp_patterns_get_pattern_data(a)
        rmspace = string.maketrans(" ","_")
        pname = string.translate(name, rmspace,'()#,!')
        new_width = 32
        new_height = 32
        if width < height:
            sides = height
        else: 
            sides = width
        image = pdb.gimp_image_new(sides,sides, RGB)
        drawable = gimp.layer(image, a, sides, sides, RGBA_IMAGE, 100, 0)
        image.add_layer(drawable, 0)
        sample_merged = 0
        pdb.gimp_edit_fill(drawable, BG_IMAGE_FILL)
        pdb.gimp_bucket_fill(drawable, PATTERN_BUCKET_FILL, NORMAL_MODE, 100, 255, sample_merged, 0, 0)
        pdb.gimp_image_scale(image, new_width, new_height)
        pdb.gimp_file_save(image, drawable, page_location + pname + '.png', pname + '.png')
        pdb.gimp_image_delete(image)
        f.write('<div><img src="' + pname + '.png" width="32" height="32" alt="pattern sample"><p>' + name + '</p></div>\n')
        if count == half:
            f.write('<div><p>half way point</p></div>\n') 
    f.write('\n') 
    f.write('<!--#include virtual="/includes/linkbar.inc" -->\n') 
    f.write('<!--#include virtual="/includes/footer.inc" -->\n') 
    f.close()
    pdb.gimp_patterns_set_pattern(old_pat)
register(
	"python_fu_mgo_patterns_xhtml",
	"Writes a resource web page and generates the sample images",
	"Writes a resource web page and generates the sample images",
	"Carol Spears",
	"Carol Spears",
	"2002",
	"<Toolbox>/Xtns/Python-Fu/mgo/patterns",
	"RGB*, GRAY*",
	[
		(PF_COLOR, "bg_colour", "background", (255,255,255)),
		(PF_COLOR, "fg_colour", "foreground", (0,0,0)),
        (PF_FILE, "page_location", "page_location", "/tmp/webwork/resources/patterns/")
	],
	[],
	write_pattern_page)

main()
