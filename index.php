<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <title>GIMP - The GNU Image Manipulation Program</title>
    <link rel="stylesheet" type="text/css" href="style/default.css"/>
  </head>
 
  <body>

    <div id="titlebar"><img id="titlebarleft" src="images/thegimp.png" alt=""/><img id="titlebarright" src="images/wilberright.png" alt=""/></div>

    <table id="layout">
      <tr>
        <td id="menu">
          <a href="?page=news">News</a><br/>
          <a href="?page=about">About GIMP</a><br/>
          <a href="?page=resources">Resources</a><br/>
          <a href="?page=registry">Plug-In Registry</a><br/>
          <a href="?page=doc">Documentation</a><br/>
          <a href="?page=tutorials">Tutorials</a><br/>
          <a href="?page=script">Script Authoring</a><br/>
          <a href="?page=devel">Development</a><br/>
          <br/>
          <a href="?page=unix">GIMP for Unix</a><br/>
          <a href="?page=win32">GIMP for Windows</a><br/>
          <a href="?page=mac">GIMP for Macintosh</a><br/>
          <br/>
          Newest Plug-Ins:<br/>
          <a href="1">Gaussian blur * (1.0)</a><br/>
          <a href="1">PSD Import/Export (2.7)</a><br/>
        </td>

        <td id="main">
          <?php
            if (!isset ($page))
              $page = "news";
            switch ($page) {
              case "about":
                $file = "includes/about.inc";
                break;
              default:
              case "news":
                $file = "includes/news.inc";
                break;
            }
            @include ($file);
          ?>
        </td>
      </tr>
    </table>
    
    <div id="linkbar">
      GIMP Links :
      <span class="linkitem"><a href="1">GIMP User Group</a></span>
      <span class="linkitem"><a href="1">Grokking With the GIMP</a></span>
      <span class="linkitem"><a href="1">Mailing Lists</a></span>
      <span class="linkitem"><a href="1">FAQ's</a></span>
      <span class="linkitem"><a href="1">GIMP Books</a></span>
    </div>

    <div>
      <span id="footerleft">
        &copy; 2001-2002 The GIMP Team
      </span>
      <span id="footerright">
        <a href="mailto:webmaster@gimp.org">webmaster@gimp.org</a>
      </span>
    </div>

  </body>
</html>
