
%.html: %.ssi
	programmatic/tools/ssi-pp.py --DocumentRoot=${DocumentRoot} --output=$@ $<

%.xhtml: %.ssi
	programmatic/tools/ssi-pp.py --DocumentRoot=${DocumentRoot} --output=$@ $<

TARGETS=example.xhtml

all: ${TARGETS}

install: all

clean:
	/bin/rm -f ${TARGETS}