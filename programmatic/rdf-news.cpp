/* -*- css -*- */
#include "wgo-css.cpp"

rss, channel, item, title, description, link {
  display: block;
}

channel, item {
  background: WGO_NEWS_INDEX_BG;
  border:     2px solid black;
  font-size:  small;
  margin-top: 3px;
  padding:    5px;
  width:      50em;
  z-index:    1;
}

RDF {
  
}

channel > title {
  background:     WGO_BLUE none;
  color:          white;
  font-family:    sans-serif;
  font-size:      large;
  font-weight:    bold;
  padding-bottom: 0.5em;
  padding-left:   1em;
  text-align:     center;
}

channel > description {
  font-family: serif;
  font-size:   1.2em;
  font-style:  italic;
  margin-top:  1em;
}

item > title {
  background:    WGO_BLUE none;
  color:         white;
  font-family:   sans-serif;
  font-size:     medium;
  margin-bottom: .5em;
  margin-top:    .5em;
  padding-left:  1em;
  text-align:    left;
}

date {
  margin-left: 1em;
}

link {
  margin-left:     1em;
  text-decoration: none;
}
