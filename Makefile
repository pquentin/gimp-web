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

SSISOURCES=$(shell find . -name '*.ssi' -print)
SSITARGETS=$(SSISOURCES:.ssi=.html)

TARGETS=${RWTARGETS} ${SSITARGETS}

.PHONY: all usage webtools install clean cvsignore programmatic

all: usage webtools ${TARGETS}
	rsync -rlt --delete --exclude-from=install.exclude ./ ${DocumentRoot}
	echo ${TARGETS}

usage:
	@if [ ${DocumentRoot}x = "x" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot>  target"; exit 1; fi

webtools:
	make -C programmatic webtools

programmatic:
	make -C programmatic all

install: all
	make -C programmatic install

clean:
	make -C programmatic clean
	rm -f ${TARGETS}

cvsignore:
	@for i in ${TARGETS} ; do basename $${i} >> `dirname $${i}`/.cvsignore ; done
	@for i in `find -name '.cvsignore' -print` ; do sort -u $${i} -o $${i}  ;	done
