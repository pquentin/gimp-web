/* -*- css -*- */
#include "wgo-css.cpp"

input[type="text"] {
 background: WGO_BUTTON_BG none;
 border: thin solid black;
 color: black;
 display: inline;
 font-family: arial,helvetica,sans-serif;
 font-weight: bold;
 text-indent: .25em;
 width: 100%;
}

input[type="button"], input[type="submit"], input[type="file"] {
 background: WGO_BUTTON_BG none;
 border-bottom: 1px solid WGO_BUTTON_LOLITE;
 border-left: 1px solid   WGO_BUTTON_HILITE;
 border-right: 1px solid  WGO_BUTTON_LOLITE;
 border-top: 1px solid    WGO_BUTTON_HILITE;
 color: WGO_BUTTON_FG;
 cursor: pointer;
 font-family: arial,helvetica,sans-serif;
 font-size: small;
 font-weight: bold;
 text-decoration: none;
}

input[type="submit"]:hover {
  text-decoration: underline;
}

.watermark { 
  background: WGO_BG;
  color: WGO_BG;
  float: left;
 }

/* my line drawing hacks and experiments */
table.ld {
  empty-cells: show;
  font-size: 1px;
  font-size: 1px;
  height: 100%;
  margin: 0px;
  padding: 0px;
  text-align: center;
  vertical-align: middle;
  visibility: visible;
  width: 100%;
}

table.ld td { text-align: center;
 border-color: black;
 border-width 0px 0px 0px 0px;
 font-size: 2px;
 margin: 0;
 padding: 0;
 vertical-align: middle;
 visibility: visible;
}

table.ld td.l----- { padding: 1px 1px 1px 1px; border-width: 0px 0px 0px 0px; border-style: solid; }
table.ld td.l----x { padding: 1px 1px 1px 0px; border-width: 0px 0px 0px 1px; border-style: solid; }
table.ld td.l---x- { padding: 1px 1px 0px 1px; border-width: 0px 0px 1px 0px; border-style: solid; }
table.ld td.l---xx { padding: 1px 1px 0px 0px; border-width: 0px 0px 1px 1px; border-style: solid; }
table.ld td.l--x-- { padding: 1px 0px 1px 1px; border-width: 0px 1px 0px 0px; border-style: solid; }
table.ld td.l--x-x { padding: 1px 0px 1px 0px; border-width: 0px 1px 0px 1px; border-style: solid; }
table.ld td.l--xx- { padding: 1px 0px 0px 1px; border-width: 0px 1px 1px 0px; border-style: solid; }
table.ld td.l--xxx { padding: 1px 0px 0px 0px; border-width: 0px 1px 1px 1px; border-style: solid; }
table.ld td.l-x--- { padding: 0px 1px 1px 1px; border-width: 1px 0px 0px 0px; border-style: solid; }
table.ld td.l-x--x { padding: 0px 1px 1px 0px; border-width: 1px 0px 0px 0px; border-style: solid; }
table.ld td.l-x-x- { padding: 0px 1px 0px 1px; border-width: 1px 0px 1px 0px; border-style: solid; }
table.ld td.l-x-xx { padding: 0px 1px 0px 0px; border-width: 1px 0px 1px 1px; border-style: solid; }
table.ld td.l-xx-- { padding: 0px 0px 1px 1px; border-width: 1px 1px 0px 0px; border-style: solid; }
table.ld td.l-xx-x { padding: 0px 0px 1px 0px; border-width: 1px 1px 0px 1px; border-style: solid; }
table.ld td.l-xxx- { padding: 0px 0px 0px 1px; border-width: 1px 1px 1px 0px; border-style: solid; }
table.ld td.l-xxxx { padding: 0px 0px 0px 0px; border-width: 1px 1px 1px p1x; border-style: solid; }
