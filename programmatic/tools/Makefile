include ../Makefile.defs

.PHONY: all clean

all: rewrite_attrs ssi-pp gimpwebtool

rewrite_attrs: rewrite_attrs.py
	sed -e 's|$${SRCDIR}|${SRCDIR}|g' -e 's|$${PYTHON}|${PYTHON}|g' $< > $@
	chmod 755 $@

ssi-pp: ssi-pp.py
	sed -e 's|$${SRCDIR}|${SRCDIR}|g' -e 's|$${PYTHON}|${PYTHON}|g' $< > $@
	chmod 755 $@

gimpwebtool: gimpwebtool.py
	sed -e 's|$${SRCDIR}|${SRCDIR}|g' -e 's|$${PYTHON}|${PYTHON}|g' $< > $@
	chmod 755 $@

clean:
	/bin/rm -f *.pyc *~ rewrite_attrs ssi-pp
