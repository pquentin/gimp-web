//images

function roundCorners () {
	$("#linkbar").corner("12px bottom");
	$("#menu").corner("14px bl");
	$("#title").corner("12px top")
}

function mangleforIE() {
	//alert("ohno!");
}

function mangleforOpera() {
  var link = document.createElement('link');
  link.type = 'text/css';
  link.rel = 'stylesheet';
  link.href = '/style/opera.css';
  $('head').append(link);

  //if there's no splash, add padding. yes it's so eeky.
  if (!$('div.splash').text()) {
    $("#menu").css("margin","0 0 1em 1em");
  }
}

//provide download page depending on OS
function renderDownload() {
	$("#downloads").html("<div id=\"os\">&nbsp;</div>\n<hr />\n<div id=\"source\">&nbsp;</div>\n");
	$("#os").load($.browser.OS + ".xhtml"); //OS specific
	$("#source").load("source.xhtml"); //sources for all
}

var usertyped = ""; //for the easteregg

function easterEgg(key) {
	var keychar = String.fromCharCode(key.charCode);
	usertyped += keychar;
	if (usertyped.indexOf("eek")!=-1) {
		var splash = "<img id=\"eek\" style=\"width: 300px; height: 400px; ";
		splash += "display: block; position: fixed;";
		splash += "top: 50%; left: 50%; margin: -200px 0 0 -150px;\"";
		splash += " src=\"/about/splash/images/eek.png\" alt=\"eeeeek!\" />";
		$("body").append(splash);
		$("#eek").click( function () {
			$(this).fadeOut()
		});
		usertyped = "";
	}
	if (key.keyCode==27) {
		$("#eek").fadeOut();
	}
}



$(document).ready(function() {
	$("#menu").hide().fadeIn(2000);
	roundCorners();
	if($.browser.msie) {
		mangleforIE();
  } else if ($.browser.opera) {
    mangleforOpera();
  }
	$(document).keypress(function (key) {
		easterEgg(key);
	});
});
