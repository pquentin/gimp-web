/* -*- css -*- */
#include "wgo-css.cpp"

.splash-image {
  background: transparent none;
  color: InfoText;
  margin-left: auto;
  margin-right: auto;
}

.splash-image a {

}

.splash-image img {
  background: Background none;
  color: InfoText;
  padding: 1px 1px 1px 1px;
}

.splash-image#preview img {
  background: black url(images/gimp-bg.png);
  color: InfoText;
  border: 2px solid red;
}

.splash-image .title {
  background: WGO_CONTEST_IMAGE_TITLE_BG;
  color:  WGO_CONTEST_IMAGE_TITLE_FG;
  font-family: sans-serif;
  font-size: medium;
  font-style: italic;
  font-weight: bold;
  margin: 0 0 0 0;
}

.splash-image .author {
  text-align: left;
  font-family: sans-serif;
  font-size: medium;
  font-style: italic;
  font-weight: bold;
}

.splash-image .email {
  text-align: right;
  font-family: sans-serif;
  font-size: medium;
  font-style: normal;
  font-weight: bold;
}


.splash-thumb { 
  font-family: sans-serif;
  border: none;
  width: 150px;
}

.splash-thumb img {
  background: black url(images/gimp-bg.png);
  color: white;
  border: none;
}

.splash-thumb#preview img {
  background: black url(images/gimp-bg.png);
  color: white;
  border: 2px solid red;
}

.splash-thumb .title {
  font-style: italic;
  font-weight: bold;
  font-size: small;
  text-align: left;
  margin: 0 0 0 0;
}

.splash-thumb .author {
  text-align: left;
  font-size: x-small;
  font-style: italic;
  font-weight: bold;
}

.splash-thumb .email {
  text-align: right;
  font-size: x-small;
  font-style: normal;
  font-weight: bold;
}

.splash-thumb input { 
  font-size: 10px;
  font-style: normal;
  font-weight: normal;
}



table.gallery {
  background: transparent none;
  color: black;
		border-width: 0px;
}

table.gallery td {
 vertical-align: top;
 /*background-image: url(/contest/images/gimp-bg.png);*/
 background-image: none;
 text-align: center;
}

table.gallery div {

}

table.gallery a {
  background: transparent none;
  color: black;
}


select { 
  font-family: sans-serif;
  background: transparent none;
  color: black;
}

table {
  width: 100%;
 }

table th { 
  text-align: left;
}


table.contest-progress-bar {
		width: 100%;
		font-size: large;
		padding: 0;
		border-spacing: 0;
		border-collapse: collapse;
		border: 1px solid black;
		border-top: none;
		margin-bottom: 1em;
}

table.contest-progress-bar a {
		display: block;
}

table.contest-progress-bar td {
		width: 1%;
		border: none;
}

table.contest-progress-bar td#current-position {
		width: 1%;
		border: 1px solid gray;
		background: none WGO_BLUE;
}

table.contest-progress-bar td#prev,
table.contest-progress-bar td#next {
		/*border: 1px solid black;*/
		font-size: normal;
		font-weight: bold;
}

table.contest-image-gallery { 
		border-spacing: 6;
		padding: 0;
		border: none;
}

table.splash-slideshow {

}

table.splash-slideshow td + td {
		width: 100%;
		text-align: left;
		font-size: xx-large;
}
