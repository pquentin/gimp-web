# This Makefile can be used to rebuild authors.htrw using the latest version
# of authors.xml found in the GIMP source tree.
# 
# You need a recent checkout of the GIMP source tree in order to run this.
# You also need xsltproc.  This is why you have to run this explicitely;
# it is not included from the top-level Makefile.
#

top_srcdir = ..

# Location of the GIMP source tree.  You can override this by running
#   make GIMP_SRCDIR=/path/to/gimp/svn/
#
GIMP_SRCDIR = $(top_srcdir)/../gimp

XSLTPROC = /usr/bin/xsltproc


all: authors.htrw

authors.htrw: $(GIMP_SRCDIR)/authors.xml authors.xsl
	$(XSLTPROC) authors.xsl $< > $(@) || rm -f $(@)
