// JavaScript code for www.gimp.org
// $Id$

var main_el;
var menu_el;
var button_el;
var menu_shown = true;

if (document.getElementById) {
  // W3C DOM
  main_el = document.getElementById("main");
  menu_el = document.getElementById("menu");
  button_el = document.getElementById("menubutton");
} else if (document.all) {
  // IE4 DOM
  main_el = document.all["main"];
  menu_el = document.all["menu"];
  button_el = document.all["menubutton"];
}

function adjust_menu () {
  var padding = 10;
  if (menu_el && main_el) {
    if (main_el.offsetHeight && menu_el.offsetHeight) {
      if (main_el.offsetHeight > menu_el.offsetHeight) {
        menu_el.style.height = (main_el.offsetHeight - 2 * padding) + "px";
      } else {
        main_el.style.height = (menu_el.offsetHeight - 2 * padding) + "px";
      }
    }
    if (menu_el.offsetWidth) {
      main_el.style.marginLeft = (menu_el.offsetWidth + padding) + "px";
    }
  }
}

function toggle_menu () {
  if (menu_shown) {
    if (menu_el) {
      menu_el.style.display = "none";
    }
    if (main_el) {
      main_el.style.marginLeft = "0px";
    }
    menu_shown = false;
  } else {
    if (menu_el) {
      menu_el.style.display = "block";
    }
    menu_shown = true;
    adjust_menu ();
    if (button_el) {
      // Small hack because zIndex does not always work
      button_el.style.display = "none";
      button_el.style.display = "block";
    }
  }
}

adjust_menu ();
