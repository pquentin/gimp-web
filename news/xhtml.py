#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-

import types
import string
import sys
import os
from UserDict import *

color = {}

def escape(s, quote=None):
  s = string.replace(s, "%", "%25")
  s = string.replace(s, "&", "%26")
  s = string.replace(s, "<", "%3C")
  s = string.replace(s, ">", "%3E")
  if quote:
    s = string.replace(s, '"', "%22")
    pass
  return s
  
def environ():
  l = os.environ.keys()
  l.sort()
  map(lambda k: sys.stdout.write("%s=%s<br />" % (k, escape(os.environ[k]))), l)
  return (None)

def validate(text = "."):
  if os.environ.has_key("SERVER_ADDR") and os.environ.has_key("SERVER_PORT") and os.environ.has_key("REQUEST_URI"):
    url = escape("http://" + os.environ["SERVER_ADDR"] \
                 + ":" + os.environ["SERVER_PORT"] \
                 + os.environ["REQUEST_URI"])
    
    uri = "http://validator.w3.org/check?url=" + url
    return (div(hyperlink(text, {"href" :uri})))

  return ("")

                            
def _isinstance(thing, *others):
    for i in others:
        if isinstance(thing, i):
            return 1
    return 0

class html_attrs(UserDict):
    def __init__(self, attrs):
        UserDict.__init__(self, attrs)
        return None

    def __repr__(self):
        str = ""
        k = self.data.keys()
        k.sort()

        for a in k:
            if self.data[a] == "" or self.data[a] == None:
                str += ' %s' % (a)
            else:
                str += ' %s="%s"' % (a, self.data[a])
                    
        return str

class xyz_init:
    def __init__(self, attrs, begin="<??%s>"):
        self.begin = begin
        self.a = html_attrs(attrs)
        return None

    def __repr__(self):
        return self.begin % (self.a)
    
class xyz_fini:
    def __init__(self, tag="</??>"):
        self.tag = tag
        return None

    def __repr__(self):
        return self.tag

class __html__:
    def __init__(self, content, attrs, begin="<??%s>", end="</??>"):
        self.begin = begin
        self.end = end
        self.a = html_attrs(attrs)

        if type(content) == types.NoneType:
            self.content = ""
        elif type(content) == types.StringType:
            self.content = content
        elif type(content) == types.FileType:
            self.content = ""
            self.readfile(content)
        else:
            #self.content = "%s" % (content)
            self.content = content
            pass

        return None

    def __coerce__(self, other):
        return ("%s" % (self), ("%s" % (other)))
    
    def __repr__(self):
        return self.begin % (self.a) + "%s" % (self.content) + self.end

    def __add__(self, other):
        print >>sys.stderr, "add self, other", type(self), type(other)
        return __html__("%s%s" % (self, other), {})

    def attribute(self, name, value):
        self.a[name] = value
        return self

    def readfile(self, input):
        if type(input) == types.StringType:
            input = open(input)
        for l in input.read():
            self.content += l
            pass

        return self

class debug(__html__):
    def __init__(self, content=None, attrs={}):
        print >>sys.stderr, content
        return None

class include(__html__):
    def __init__(self, filename):
        fp = open(filename, "r")
        content =  fp.read()
        fp.close()
        __html__.__init__(self, content, {}, "", "")
        return

class xml(__html__):
    def __init__(self, attrs={"version" : "1.0", "encoding" : "iso-8859-1"}):
        __html__.__init__(self, None, attrs, '<?xml%s?>', "")
        return
    
class doctype(__html__):
    def __init__(self):
        __html__.__init__(self, None, {}, '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">', "")
        return
    
class body(__html__):
    defaults = {}

    def __init__(self, content=None, attrs={}):
        a = dict(self.defaults)
        a.update(attrs)
        __html__.__init__(self, content, a, "<body%s>", "</body>")
        return None

    class init(xyz_init):
        def __init__(self, attrs={}):
            return (xyz_init.__init__(self, attrs, "<body%s>"))

    class fini(xyz_fini):
        def __init__(self, attrs={}):
            return (xyz_fini.__init__(self, "</body>"))

class title(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "<title%s>", "</title>")
        return None

class html(__html__):
    def __init__(self, content=None, attrs={}):
        return (__html__.__init__(self, content, attrs, "<html%s>", "</html>"))

    class init(xyz_init):
        def __init__(self, attrs={}):
            return (xyz_init.__init__(self, attrs, "<html%s>"))

    class fini(xyz_fini):
        def __init__(self, attrs={}):
            return (xyz_fini.__init__(self, "</html>"))
    
class link(__html__):
    defaults = { "rel": "stylesheet",
                 "href": "#",
                 "type": "text/css" }
    def __init__(self, content=None, attrs={}):
        a = dict(self.defaults)
        a.update(attrs)
        __html__.__init__(self, content, a, "<link%s>", "</link>")
        return None

class hyperlink(__html__):
    def __init__(self, content=None, attrs={"href": "#"}):
        __html__.__init__(self, content, attrs, "<a%s>", "</a>")
        return None

class mailto(__html__):
    def __init__(self, content=None, attrs={}):
        attrs = {"href" : "mailto:" + content}
        __html__.__init__(self, content, attrs, "<a%s>", "</a>")
        return None

class comment(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "<!--", " -->")
        return None

class list(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "<ul%s>", "</ul>")
        return None

    class item(__html__):
        def __init__(self, content=None, attrs={}):
            __html__.__init__(self, content, attrs, "<li%s>", "</li>")
            return None

class div(__html__):
    defaults = { }

    def __init__(self, content=None, attrs={}):
        a = dict(self.defaults)
        a.update(attrs)
        __html__.__init__(self, content, a, "<div%s>", "</div>")
        return None

    class init(xyz_init):
        def __init__(self, attrs={}):
            return (xyz_init.__init__(self, attrs, "<div%s>"))

    class fini(xyz_fini):
        def __init__(self, attrs={}):
            return (xyz_fini.__init__(self, "</div>"))


class span(__html__):
    defaults = { }

    def __init__(self, content=None, attrs={}):
        a = dict(self.defaults)
        a.update(attrs)
        __html__.__init__(self, content, a, "<span%s>", "</span>")
        return None

class para(__html__):
    defaults = { }

    def __init__(self, content=None, attrs={}):
        a = dict(self.defaults)
        a.update(attrs)
        __html__.__init__(self, content, a, "<p%s>", "</p>")
        return None

    class init(xyz_init):
        def __init__(self, attrs={}):
            return (xyz_init.__init__(self, attrs, "<p%s>"))

    class fini(xyz_fini):
        def __init__(self, attrs={}):
            return (xyz_fini.__init__(self, "</p>"))

class dd(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "<dd%s>", "</dd>")
        return None

class dl(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "<dl%s>", "</dl>")
        return None

class dt(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "<dt%s>", "</dt>")
        return None

class head(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "<head%s>", "</head>")
        return None

    class init(xyz_init):
        def __init__(self, attrs={}):
            return (xyz_init.__init__(self, attrs, "<head%s>"))

    class fini(xyz_fini):
        def __init__(self, attrs={}):
            return (xyz_fini.__init__(self, "</head>"))

class text(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "", "")
        return None

    def __repr__(self):
        return self.content

class table(__html__):
    defaults = {"summary": "table"}

    def __init__(self, content=None, attrs={}):
        assert _isinstance(content, __html__, table.row, types.StringType)
        a = dict(self.defaults)
        a.update(attrs)

        __html__.__init__(self, content, a, "<table%s><tbody>", "</tbody></table>")
        return None

    class init(xyz_init):
        def __init__(self, attrs={}):
            a = dict(table.defaults)
            a.update(attrs)
            return (xyz_init.__init__(self, a, "<table%s><tbody>"))

    class fini(xyz_fini):
        def __init__(self, attrs={}):
            return (xyz_fini.__init__(self, "</tbody></table>"))

    class row(__html__):
        def __init__(self, content=None, attrs={}):
            assert _isinstance(content, __html__, table.cell, types.StringType)
            __html__.__init__(self, content, attrs, "<tr%s>", "</tr>")
            return None

        class init(xyz_init):
            def __init__(self, attrs={}):
                return (xyz_init.__init__(self, attrs, "<tr%s>"))

        class fini(xyz_fini):
            def __init__(self, attrs={}):
                return (xyz_fini.__init__(self, "</tr>"))

    class cell(__html__):
        def __init__(self, content=None, attrs={}):
            self.attributes = attrs
            __html__.__init__(self, content, self.attributes, "<td%s>", "</td>")
            return None

        class init(xyz_init):
            def __init__(self, attrs={}):
                return (xyz_init.__init__(self, attrs, "<td%s>"))

        class fini(xyz_fini):
            def __init__(self, attrs={}):
                return (xyz_fini.__init__(self, "</td>"))

    class header(__html__):
        def __init__(self, content=None, attrs={}):
            __html__.__init__(self, content, attrs, "<th%s>", "</th>")
            return None

class image(__html__):
    defaults = {"alt" : ""}
    def __init__(self, attrs={}):
        a = dict(self.defaults)
        a.update(attrs)
        __html__.__init__(self, "", a, "<img%s />", "")
        return None

class linebreak(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "", "<br />\n")
        return None

class script(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "<script%s>", "</script>\n")
        return None

class pre(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, xhtml_escape(content), attrs, "<pre%s>", "</pre>\n")
        return None

class input(__html__):
    defaults = {"type": "submit", "name": "submit"}
    allowed = {"type":
               ("text", "password", "checkbox", "radio", "submit",
                "reset", "file", "hidden", "image", "button")}
    def __init__(self, attrs=defaults):
        __html__.__init__(self, "", attrs, "<input%s />\n", "")
        return None

    class hidden(__html__):
        def __init__(self, attrs={}):
            __html__.__init__(self, "", attrs, '<input type="hidden"%s />\n', "")
            return None
    
    class submit(__html__):
        def __init__(self, attrs={}):
            __html__.__init__(self, "", attrs, '<input type="submit"%s />\n', "")
            return None

    class checkbox(__html__):
        def __init__(self, attrs={}):
            __html__.__init__(self, "", attrs, '<input type="checkbox"%s />\n', "")
            return None

    class text(__html__):
        defaults = { }
        def __init__(self, attrs=defaults):
            __html__.__init__(self, "", attrs, '<input type="text"%s />', "")
            return None

    class button(__html__):
        defaults = { }
        def __init__(self, content=None, attrs=defaults):
            __html__.__init__(self, content, attrs, "<button%s>", "</button>\n")
            return None

    class textarea(__html__):
        defaults = { }
        def __init__(self, content=None, attrs=defaults):
            __html__.__init__(self, content, attrs, "<textarea%s>", "</textarea>\n")
            return None

    class select(__html__):
        defaults = { }
        def __init__(self, content=None, attrs=defaults):
            __html__.__init__(self, content, attrs, "<select%s>\n", "</select>\n")
            return None
    
    class option(__html__):
        defaults = { }
        def __init__(self, content=None, attrs=defaults):
            __html__.__init__(self, content, attrs, "<option%s>", "</option>\n")
            return None
        
    
class form(__html__):
    defaults = { }
    def __init__(self, content=None, attrs=defaults):
        __html__.__init__(self, content, attrs, "<form%s>\n", "</form>\n")
        return None

    class init(xyz_init):
        def __init__(self, attrs={}):
            return (xyz_init.__init__(self, attrs, "<form%s>"))

    class fini(xyz_fini):
        def __init__(self, attrs={}):
            return (xyz_fini.__init__(self, "</form>"))

class meta(__html__):
    defaults = { }
    def __init__(self, content=None, attrs=defaults):
        __html__.__init__(self, content, attrs, "<meta%s />", "\n")
        return None

class style(__html__):
    defaults = {"type": "text/css" }
    def __init__(self, content=None, attrs=defaults):
        __html__.__init__(self, content, attrs, "<style%s>\n", "</style>\n")
        return None

    class css(__html__):
        def __init__(self, selector, style={}):
            self.selector = selector
            self.style = style
            return None

        def __repr__(self):
            out = self.selector + " { "
            for s in self.style.keys():
                out += '%s: %s; ' % (s, self.style[s])
            out += "}"
            return out

class php(__html__):
    defaults = { }
    def __init__(self, content=None, attrs=defaults):
        __html__.__init__(self, content, attrs, "<?php", "?>")
        return None

class extn(__html__):
    def __init__(self):
        return None

def _load_rgb():
    _input = open("/usr/lib/X11/rgb.txt")
    _input.readline()
    for _line in _input.readlines():
        _s = _line.split()
        color.update({ string.joinfields(_s[3:]):
                       "#%02x%02x%02x" % (int(_s[0]), int(_s[1]), int(_s[2]))})

    _input.close()

_load_rgb()

def _dump_colors():
    keys = color.keys()
    keys.sort()

    rows = ""
    for k in keys:
        row = table.row(table.cell("%s %s" % (color[k], k), {"bgcolor": color[k]})
                        + table.cell("%s %s" % (color[k], k), {"bgcolor": "white"}))
        rows += row.__repr__()

    print table(rows)
