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
	chmod 755 $@

RWSOURCES=$(shell find . -name '*.htrw' -print)
RWTARGETS=$(RWSOURCES:.htrw=.html)

TARGETS=${RWTARGETS}

all: usage webtools ${TARGETS}
	echo ${TARGETS}

usage:
	@if [ ${DocumentRoot}x = "x" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot>  target"; exit 1; fi

webtools:
	(cd programmatic ; make webtools)

_install: all

clean:
	/bin/rm -f ${TARGETS}