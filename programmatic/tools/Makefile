include ../Makefile.defs

all: rewrite_attrs

rewrite_attrs: rewrite_attrs.py
	sed -e 's|$${SRCDIR}|${SRCDIR}|g' -e 's|$${PYTHON}|${PYTHON}|g' $< > $@
	chmod 755 $@

clean:
	/bin/rm -f *.pyc *~ rewrite_attrs
