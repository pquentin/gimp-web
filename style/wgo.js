// JavaScript code for www.gimp.org - Copyright (C) 2003, Raphael Quinet
// $Id$

var main_el;
var menu_el;
var button_el;
var menu_shown = true;

function menu_adjust () {
  var padding = 10;
  if (menu_el && main_el) {
    // adjust the height of the menu to match the height of the contents
    if (main_el.offsetHeight && menu_el.offsetHeight) {
      if (main_el.offsetHeight > menu_el.offsetHeight) {
        menu_el.style.height = (main_el.offsetHeight - 2 * padding) + "px";
      } else {
        main_el.style.height = (menu_el.offsetHeight - 2 * padding) + "px";
      }
    }
    // adjust the position of the contents to match the width of the menu
    if (menu_el.offsetWidth) {
      if (menu_el.offsetWidth > 100) {
        main_el.style.marginLeft = (menu_el.offsetWidth + padding) + "px";
      } else {
        main_el.style.marginLeft = "11em";
      }
    }
  }
}

function menubutton_raise () {
  if (button_el) {
    // Small hack because zIndex does not work in all cases
    button_el.style.display = "none";
    button_el.style.display = "block";
  }
}

function menu_hide () {
  if (menu_el) {
    menu_el.style.display = "none";
  }
  if (main_el) {
    main_el.style.marginLeft = "0px";
  }
  menu_shown = false;
}

function menu_show () {
  if (menu_el) {
    menu_el.style.display = "block";
  }
  menu_shown = true;
  menu_adjust ();
  menubutton_raise ();
}

function menu_toggle () {
  if (menu_shown) {
    menu_hide ();
  } else {
    menu_show ();
  }
}

function wgo_init (show_menu) {
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
  if (show_menu != false) {
    menu_show ();
  } else {
    menu_hide ();
  }
}

if (document.getElementById || document.all) {
  document.write('<div id="menubutton"><img src="/images/menubutton.png" alt="" border="0" onclick="menu_toggle();" /></div>');
}
