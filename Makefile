#
#

export PYTHONPATH=$(shell pwd)/programmatic:

# how to make an html from a .htrw file
%.html: %.htrw
	programmatic/tools/ssi-pp --DocumentRoot=${DocumentRoot} --output=$<.x $<
	programmatic/tools/rewrite_attrs -d admin/gimp-web-urls  $<.x > $@
	rm -f $<.x

SOURCES=$(shell find . -name '*.htrw' -print)
TARGETS=$(SOURCES:.htrw=.html)

.PHONY: all usage webtools mirrors install clean cvsignore programmatic includes crontab target

all: usage includes webtools mirrors crontab ${TARGETS}
	rsync -rlt --delete --exclude-from=install.exclude ./ ${DocumentRoot}
	echo ${TARGETS}

includes:
	rsync -rlt --delete --exclude-from=install.exclude includes ${DocumentRoot}

usage:
	@if [ ${DocumentRoot}x = "x" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot>  target"; exit 1; fi

target:
	@echo "Choose a target among: clean, all, install or cvsignore"; exit 1

mirrors:
	make -C programmatic downloads
	make -C programmatic install-downloads

webtools:
	make -C programmatic webtools

programmatic:
	make -C programmatic all

crontab:
	make -C crontab all

install: all
	make -C programmatic install
	make -C crontab install

clean:
	make -C programmatic clean
	rm -f ${TARGETS}

cvsignore:
	@for i in ${TARGETS} ; do basename $${i} >> `dirname $${i}`/.cvsignore ; done
	@for i in `find -name '.cvsignore' -print` ; do sort -u $${i} -o $${i}  ;	done
