//images

function roundCorners () {
	$("#linkbar").corner("7px bottom");
	$("#menu").corner("14px bl");
}

function mangleforIE() {
	//alert("ohno!");
}

//provide download page depending on OS
function renderDownload() {
	return $.browser.OS;
}

$(document).ready(function() {
	$("#menu").fadeIn(2000);
	roundCorners();
	if($.browser.msie) {
		mangleforIE();
	};
	$("#downloads").empty().append(renderDownload());
})
