# FIXME: This Makefile is not very clean.  It should be rewritten
# using autoconf or at least using a similar style:
# - one Makefile per directory (taking care of the files in that
#   directory only),
# - keep a clear difference between recursive and non-recursive rules,
# - always use target names consistently ("make mirrors" should not
#   "make something else" in another directory),
# - do not process directories more than once during "make all",
# - no rules except "make install" should install files (all other
#   rules should only work in the source directories).
#

TOOLSDIR?=programmatic/tools

export PYTHONPATH=$(shell pwd)/programmatic:

# how to make an html from a .htrw file
#%.html: %.htrw
#	programmatic/tools/ssi-pp --DocumentRoot=${DocumentRoot} --output=$<.x $<
#	programmatic/tools/rewrite_attrs -d admin/gimp-web-urls  $<.x > $@
#	rm -f $<.x

%.html: %.htrw
	$(TOOLSDIR)/rewrite_attrs -d admin/gimp-web-urls -q $< > $@
	chmod u+x $@ # XXX interim solution (Helvetix)
	rm -f $<.x

SOURCES=$(shell find . -name '*.htrw' -print)
TARGETS=$(SOURCES:.htrw=.html)

.PHONY: all usage webtools mirrors install clean cvsignore programmatic includes crontab target

all: usage includes webtools mirrors crontab ${TARGETS}
	rsync -rlt --omit-dir-times --exclude-from=install.exclude ./ ${DocumentRoot}
	echo ${TARGETS}

# Install all includes files to the target directory (FIXME: this should not
# be necessary anymore if SSI is disabled -- we should update ssi-pp to use
# the source directory instead of the target directory for all includes.)
#
# kludge: install includes/news.inc if it does not exist yet in the target dir
includes:
	rsync -rlt --delete --omit-dir-times --exclude-from=install.exclude includes ${DocumentRoot}
	@if [ -r ${DocumentRoot}/includes/news.inc ]; then :; else cp -p includes/news.inc ${DocumentRoot}/includes/news.inc ; fi

usage:
	@if [ ${DocumentRoot}x = "x" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot>  target"; echo "You can also set DocumentRoot in your environment."; echo "You should probably use the script install.sh to do everything at once."; exit 1; fi

target:
	@echo "Choose a target among: clean, all, install or cvsignore"; exit 1

mirrors:
	$(MAKE) -C programmatic downloads
	$(MAKE) -C programmatic install-downloads

webtools:
	$(MAKE) -C programmatic webtools

programmatic:
	$(MAKE) -C programmatic all

crontab:
	$(MAKE) -C crontab all

install: all
	$(MAKE) -C programmatic install
	$(MAKE) -C crontab install

clean:
	$(MAKE) -C programmatic clean
	rm -f ${TARGETS}

cvsignore:
	@for i in ${TARGETS} ; do basename $${i} >> `dirname $${i}`/.cvsignore ; done
	@for i in `find -name '.cvsignore' -print` ; do sort -u $${i} -o $${i}  ;	done
