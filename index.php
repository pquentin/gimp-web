<?php echo '<?xml version="1.0" encoding="iso-8859-1"?>' ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <title>GIMP - The GNU Image Manipulation Program</title>
    <link rel="stylesheet" type="text/css" href="style/default.css"/>
    
    <?php
      if (isset ($tutorial)) {
        echo '<style type="text/css">#linkbar, #menu { display: none; }</style>';
      } else {
        echo '<style type="text/css">#navbar { display: none; }</style>';
      }
    ?>

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
          <a href="?page=documentation">Documentation</a><br/>
          <a href="?page=tutorials">Tutorials</a><br/>
          <a href="?page=authoring">Script Authoring</a><br/>
          <a href="?page=development">Development</a><br/>
          <br/>
          <a href="?page=unix">GIMP for Unix</a><br/>
          <a href="?page=windows">GIMP for Windows</a><br/>
          <a href="?page=macintosh">GIMP for Macintosh</a><br/>
          <a href="?page=os2">GIMP for OS/2</a><br/>
          <br/>
          Newest Plug-Ins:<br/>
          <a href="FIXME">Gaussian blur * (1.0)</a><br/>
          <a href="FIXME">PSD Import/Export (2.7)</a><br/>
          <br/>
          <br/>
        </td>

        <td id="main">
          <?php
            if (!isset ($page))
              $page = "news";
            switch ($page) {
              case "about":
                $file = "includes/about.inc";
                break;
              case "resources":
                $file = "includes/resources.inc";
                break;
              case "registry":
                $file = "includes/registry.inc";
                break;
              case "documentation":
                $file = "includes/documentation.inc";
                break;
              case "tutorials":
                $file = "includes/tutorials.inc";
                break;
              case "authoring":
                $file = "includes/authoring.inc";
                break;
              case "development":
                $file = "includes/development.inc";
                break;

              case "unix":
                $file = "includes/unix.inc";
                break;
              case "windows":
                $file = "includes/windows.inc";
                break;
              case "macintosh":
                $file = "includes/macintosh.inc";
                break;
              case "os2":
                $file = "includes/os2.inc";
                break;

              case "links":
                $file = "includes/links.inc";
                break;
              case "team":
                $file = "includes/team.inc";
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
      <span class="linkitem"><a href="?page=links">GIMP Links</a></span>
      <span class="linkitem"><a href="http://gug.sunsite.dk">GIMP User Group</a></span>
      <span class="linkitem"><a href="http://gimp-savvy.com/BOOK/index.html">Grokking the GIMP</a></span>
      <span class="linkitem"><a href="FIXME">Mailing Lists</a></span>
      <span class="linkitem"><a href="FIXME">FAQ's</a></span>
      <span class="linkitem"><a href="FIXME">GIMP Books</a></span>
    </div>
    <div id="navbar">
      <a href="?page=<?php echo $page;?>">Go Back</a>
    </div>

    <div>
      <span id="footerleft">
        &copy; 2001-2002 <a href="?page=team">The GIMP Team</a>
      </span>
      <span id="footerright">
        <a href="mailto:webmaster@gimp.org">webmaster@gimp.org</a>
      </span>
    </div>

  </body>
</html>
