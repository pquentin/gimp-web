<?php
  $tutorial_path = "tutorials/";

  if (isset ($tutorial)) {
    /* user requested a tutorial */
    $tutorial = basename ($tutorial);
    if (is_dir ($tutorial_path . $tutorial)) {
      @include ($tutorial_path . $tutorial . "/index.inc");
    } else {
      /* tutorial not found */
      $tutorial_not_found = true;
    }
  } 

  if (!isset ($tutorial) or isset ($tutorial_not_found)) {
    /* show list of tutorials */
    echo '<div class="heading"><span class="title">Tutorials</span><span class="date"></span>&nbsp;</div>';
    echo '<div class="item">';
          
    if ($dir = opendir ($tutorial_path)) {
    while (($file = readdir ($dir)) !== false) {
      if ($file !== "." and $file !== ".." and $file !== "CVS") {
        echo '<a href="?page=' . $page . '&amp;tutorial=' . $file . '">' . $file . '</a><br/>';
      }
    }
    closedir ($dir);
  }

    echo '</div>';
  }
?>
