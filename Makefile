#
#

export PYTHONPATH=programmatic:

# how to make an html from a .ssi file
%.html: %.ssi
	programmatic/tools/ssi-pp --DocumentRoot=${DocumentRoot} --output=$@ $<

# how to make an xhtml from a .ssi file
%.xhtml: %.ssi
	programmatic/tools/ssi-pp --DocumentRoot=${DocumentRoot} --output=$@ $<

# how to make an html from a .htrw file
%.html: %.htrw
	programmatic/tools/rewrite_attrs -d admin/gimp-web-urls  $< > $@

TARGETS=example.xhtml unix/index.html

all: usage webtools ${TARGETS}

usage:
	@if [ ${DocumentRoot}x = "x" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot>  target"; exit 1; fi

webtools:
	(cd programmatic ; make webtools)

unix/index.html: unix/index.htrw


install: all

clean:
	/bin/rm -f ${TARGETS}