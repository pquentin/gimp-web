/* -*- css -*- */
#include "wgo-css.cpp"

input[type="text"] {
  background:  WGO_BUTTON_BG none;
  border:      thin solid black;
  color:       black;
  display:     inline;
  font-family: arial,helvetica,sans-serif;
  font-weight: bold;
  text-indent: 0.25em;
  width:       100%;
}

.faux-button, input[type="button"], input[type="submit"], input[type="file"] {
  background:    WGO_BUTTON_BG none;
  border-bottom: 1px solid WGO_BUTTON_LOLITE;
  border-left:   1px solid WGO_BUTTON_HILITE;
  border-right:  1px solid WGO_BUTTON_LOLITE;
  border-top:    1px solid WGO_BUTTON_HILITE;
  color:         WGO_BUTTON_FG;
  cursor:        pointer;
  font-family:   arial,helvetica,sans-serif;
  font-size:     x-small;
  font-weight:   bold;
  padding:       .1em .2em .1em .2em;
  margin:        0 0 0 0 ;
  text-decoration: none;
}

.faux-button:hover, input[type="submit"]:hover {
  text-decoration: underline;
  background:    WGO_BUTTON_BG none;
  color: WGO_BUTTON_FG;
  border-bottom: 1px solid WGO_BUTTON_LOLITE;
  border-left:   1px solid WGO_BUTTON_HILITE;
  border-right:  1px solid WGO_BUTTON_LOLITE;
  border-top:    1px solid WGO_BUTTON_HILITE;
}

.watermark { 
  background: WGO_BG;
  color:      WGO_BG;
  display:    inline;
  font-size:  8px;
}


/* my line drawing hacks and experiments */
table.ld {
  margin:         0 0 0 0;
  padding:        0 0 0 0;
  text-align:     center;
  vertical-align: middle;
  visibility:     visible;
  width:          100%;
  background: transparent none;
  border-spacing: 0;
}

table.ld tr { 
  background: transparent none !important;
}

table.ld td {
  background: transparent none !important;
  border-color:   black;
  border-style:   solid;
  border-width:   0 0 0 0;
  margin:         0 0 0 0;
  padding:        0 0 0 0;
  text-align:     center;
  vertical-align: middle;
}

table.ld td.l----- { padding: 1px 1px 1px 1px !important; border-width: 0px 0px 0px 0px !important; }
table.ld td.l----x { padding: 1px 1px 1px 0px !important; border-width: 0px 0px 0px 1px !important; }
table.ld td.l---x- { padding: 1px 1px 0px 1px !important; border-width: 0px 0px 1px 0px !important; }
table.ld td.l---xx { padding: 1px 1px 0px 0px !important; border-width: 0px 0px 1px 1px !important; }
table.ld td.l--x-- { padding: 1px 0px 1px 1px !important; border-width: 0px 1px 0px 0px !important; }
table.ld td.l--x-x { padding: 1px 0px 1px 0px !important; border-width: 0px 1px 0px 1px !important; }
table.ld td.l--xx- { padding: 1px 0px 0px 1px !important; border-width: 0px 1px 1px 0px !important; }
table.ld td.l--xxx { padding: 1px 0px 0px 0px !important; border-width: 0px 1px 1px 1px !important; }
table.ld td.l-x--- { padding: 0px 1px 1px 1px !important; border-width: 1px 0px 0px 0px !important; }
table.ld td.l-x--x { padding: 0px 1px 1px 0px !important; border-width: 1px 0px 0px 0px !important; }
table.ld td.l-x-x- { padding: 0px 1px 0px 1px !important; border-width: 1px 0px 1px 0px !important; }
table.ld td.l-x-xx { padding: 0px 1px 0px 0px !important; border-width: 1px 0px 1px 1px !important; }
table.ld td.l-xx-- { padding: 0px 0px 1px 1px !important; border-width: 1px 1px 0px 0px !important; }
table.ld td.l-xx-x { padding: 0px 0px 1px 0px !important; border-width: 1px 1px 0px 1px !important; }
table.ld td.l-xxx- { padding: 0px 0px 0px 1px !important; border-width: 1px 1px 1px 0px !important; }
table.ld td.l-xxxx { padding: 0px 0px 0px 0px !important; border-width: 1px 1px 1px 1px !important; }
