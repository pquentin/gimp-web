/* -*- css -*- */
#include "wgo-css.cpp"

select { 
  font-family: sans-serif;
  color: black;
  background: transparent none;
}

a.news-index {
  text-decoration: underline;
}

/* distill out a common look to the table for the admin/ stuff */
table.wgo-admin {
  font-size: medium;
  border: 1px solid black;
  margin-left: 40px;
  margin-right: 40px;
}

table.wgo-admin tr {

}

table.wgo-admin th {
  background: WGO_NEWS_INDEX_HEADER_BG none;
  border-right: 1px solid white;
  color: WGO_NEWS_INDEX_HEADER_FG;
  padding: 1px 0px 1px .25em;
  text-align: left;
}

table.wgo-admin td {
  background: WGO_NEWS_INDEX_BG none;
  border-bottom: 1px solid black;
  color: black;
  padding: 1px 0px 1px 0px;
  text-indent: 0.25em;
}

table.wgo-admin td input[type="checkbox"] {
  background: WGO_NEWS_INDEX_BG none;
  border-bottom: 1px solid black;
  color: black;
  text-indent: 0.25em;
}


/* ---------------- */
table.news-index {
  font-size: medium;
}

table.news-index tr {

}

table.news-index th {
  background: WGO_NEWS_INDEX_HEADER_BG none;
  border-right: 1px solid white;
  color: WGO_NEWS_INDEX_HEADER_FG;
  padding-left: 0px;
  padding-top: 1px;
  text-align: left;
}

table.news-index th#checkbox {
  border: 0px none black;
  margin: 0px 0px 0px 0px;
  padding: 0px 0px 0px 0px;
  text-align: center;
  vertical-align: middle;
}

table.news-index th#subject {
  margin: 0px 0px 0px 0px;
  padding: 0px 0px 0px 0px;
  text-indent: 0.25em;
  width: 40%;
}

table.news-index th#from {
  border-right: 1px solid white;
  margin: 0px 0px 0px 0px;
  padding: 0px 0px 0px 0px;
  text-indent: 0.25em;
  width: 35%;
}

table.news-index th#date {
  border-right: 1px solid white;
  margin: 0px 0px 0px 0px;
  padding: 0px 0px 0px 0px;
  text-indent: 0.25em;
  width: 27%;
}

table.news-index td {
  background: WGO_NEWS_INDEX_BG none;
  border-bottom: 1px solid black;
  color: black;
  text-indent: 0.25em;
}

table.news-index td:first-child {
  border-left: 1px solid black;
}

table.news-index td input[type="checkbox"] {
  background: WGO_NEWS_INDEX_BG none;
  border-bottom: 1px solid black;
  color: black;
  text-indent: 0.25em;
}

table.news-index td.control { 
  background: transparent none;
  color: WGO_NEWS_INDEX_FG;
  border-width: 0 0 0 0;
}


table.batch {
  font-size: small;
 width: 100%;
}

table.batch tr {
  background: WGO_NEWS_INDEX_BG none;
  color: black;
}

table.batch th {
  background: WGO_NEWS_INDEX_HEADER_BG none;
  border-bottom: 1px solid black;
  border-right: 1px solid white;
  color: WGO_NEWS_INDEX_HEADER_FG;
  padding-left: 2px;
  padding-top: 1px;
  text-align: left;
}

table.batch td {
  border-bottom: 1px solid black;
  background: WGO_NEWS_INDEX_BG none;
  padding-left: 2px;
  color: WGO_NEWS_INDEX_FG;
}

table.batch td#success {
  border-bottom: 1px solid black;
  background: green none;
  padding-left: 2px;
  color: black;
}

table.batch td#failure {
  border-bottom: 1px solid black;
  background: red none;
  padding-left: 2px;
  color: black;
}

table.news-edit {

}

table.news-edit td {
  font-weight: bold;
}

table.news-edit td#from {
  font-weight: bold;
  padding-left: 0.5em;
  text-indent: 0.1em;
}

table.news-edit td#message-id {
  font-weight: bold;
  padding-left: 0.5em;
  text-indent: 0.1em;
}

table.news-edit td#subject {
  font-weight: bold;
  padding-left: 0.5em;
  text-indent: 0.1em;
}

table.news-edit td#date {
  font-weight: bold;
  padding-left: 0.5em;
  text-indent: 0.1em;
}

table.news-edit td#image {
  font-weight: bold;
  padding-left: 0.5em;
  text-indent: 0.1em;
}


form.news-edit {
  margin-left: 0px;
}

form.news-edit select {
  background: WGO_NEWS_EDIT_BG none;
  color: WGO_NEWS_EDIT_FG;
  border: thin solid black;
}

form.news-edit input[name="subject"] {
  text-indent: 1em;
  background: WGO_NEWS_EDIT_BG none;
  border: thin solid black;
  color: WGO_NEWS_EDIT_FG;
  display: inline;
  font-family: arial,helvetica,sans-serif;
  font-weight: bold;
  width: 40em;
}

form.news-edit input[name="date"] {
  background: WGO_NEWS_EDIT_BG none;
  border: thin solid black;
  color: WGO_NEWS_EDIT_FG;
  display: inline;
  font-family: arial,helvetica,sans-serif;
  font-weight: bold;
  text-align: left;
  width: 20em;
}

form.news-edit textarea[name="body"] {
  background: WGO_NEWS_EDIT_BG none;
  border: thin solid black;
  color: WGO_NEWS_EDIT_FG;
  font-family: arial,helvetica,sans-serif;
  height: 20em;
  width: 100%;
}

/*
td#menu a { 
  display: block;
  }*/
