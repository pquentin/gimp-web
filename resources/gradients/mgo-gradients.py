#!/usr/bin/env python

import string
from gimpfu import *

def write_gradients_page(bg_colour, fg_colour, page_location):
    f = open(page_location + 'index.html', 'w')
    f.write('<!--#include virtual="/includes/header_pretitle.inc" -->\n')
    f.write('<title>GIMP - Resources - Patterns</title>\n')
    f.write('<!--#include virtual="/includes/header_posttitle.inc" -->\n')
    f.write('<!--#include virtual="/includes/menu.inc" -->')
    f.write('<!--This page rendered with mgo-gradients -->\n')
    f.write('<div class="heading">Resources - Gradients</div>\n') 
    f.write('<div class="subtitle">Included With The GIMP</div>\n') 
    f.write('<p>More than just a bunch of tools, The GIMP has stuff too ....</p>\n') 
    f.write('<div>this is the beginning</div>\n') 
    num_gradients, gradient_names = pdb.gimp_gradients_get_list()    
    old_grad = pdb.gimp_gradients_get_active()    
    old_pat, owidth, oheight = pdb.gimp_patterns_get_pattern()    
    half = int(round(num_gradients / 2.0))
    count = 0
    pattern = "GIMP Pattern -- transparency sm"
    for a in gradient_names:
        pdb.gimp_gradients_set_active(a)
        pdb.gimp_patterns_set_pattern(pattern)
        count += 1
        name = a
        rmspace = string.maketrans(" ","_")
        pname = string.translate(name, rmspace,'()#,!')
        width = 64
        height = 32
        sample_merged = 0
        image = pdb.gimp_image_new(width, height, RGB)
        transparency = gimp.layer(image, pattern, width, height, RGBA_IMAGE, 100, 0)
        image.add_layer(transparency, 0)
        pdb.gimp_edit_fill(transparency, BG_IMAGE_FILL)
        pdb.gimp_bucket_fill(transparency, PATTERN_BUCKET_FILL, NORMAL_MODE, 100, 255, sample_merged, 0, 0)
        drawable = gimp.layer(image, a, width, height, RGBA_IMAGE, 100, 0)
        image.add_layer(drawable, 1)
        pdb.gimp_blend(drawable, CUSTOM, NORMAL_MODE, LINEAR, 100, 0, REPEAT_NONE, FALSE, 0, 0.0, 0, 16, 64, 16)
        layer = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)
        pdb.gimp_file_save(image, drawable, page_location + pname + '.png', pname + '.png')
        pdb.gimp_image_delete(image)
        f.write('<div><img style="vertical-align: text-middle;" src="' + pname + '.png" width="64" height="32" alt="gradient sample">' + name + '</div>\n')
        if count == half:
            f.write('<div><p>half way point</p></div>\n') 
    f.write('\n') 
    f.write('<!--#include virtual="/includes/linkbar.inc" -->\n') 
    f.write('<!--#include virtual="/includes/footer.inc" -->\n') 
    f.close()
    pdb.gimp_gradients_set_active(old_grad)
    pdb.gimp_patterns_set_pattern(old_pat)
register(
	"python_fu_mgo_gradients_xhtml",
	"Writes a resource web page and generates the sample images",
	"Writes a resource web page and generates the sample images",
	"Carol Spears",
	"Carol Spears",
	"2002",
	"<Toolbox>/Xtns/Python-Fu/mgo/gradients",
	"RGB*, GRAY*",
	[
		(PF_COLOR, "bg_colour", "background", (255,255,255)),
		(PF_COLOR, "fg_colour", "foreground", (0,0,0)),
        (PF_FILE, "page_location", "page_location", "/tmp/webwork/resources/")
	],
	[],
	write_gradients_page)

main()
