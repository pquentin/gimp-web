//images

function roundCorners () {
	$("#linkbar").corner("12px bottom");
	$("#menu").corner("14px bl");
	$("#title").corner("12px top")
}

function mangleforIE() {
	//alert("ohno!");
}

//provide download page depending on OS
function renderDownload() {
	$("#downloads").html("<div id=\"os\">&nbsp;</div>\n<hr />\n<div id=\"source\">&nbsp;</diov>\n");
	$("#os").load($.browser.OS + ".xhtml"); //OS specific
	$("#source").load("source.xhtml"); //sources for all
}

$(document).ready(function() {
	$("#menu").hide().fadeIn(2000);
	$("p.intropara").click(function () {
		$(this).slideUp(2000);
	});
	roundCorners();
	if($.browser.msie) {
		mangleforIE();
	};
})
