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
	return $.browser.OS;
}

$(document).ready(function() {
	$("#menu").fadeIn(2000);
	$("p.intropara").click(function () {
		$(this).slideUp(2000);
	});
	roundCorners();
	if($.browser.msie) {
		mangleforIE();
	};
	$("#downloads").empty().append(renderDownload());
})
