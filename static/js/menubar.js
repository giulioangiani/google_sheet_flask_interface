(function($) {
	"use strict";
	var fullHeight = function() {
		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
	  if ($("#sidebar").hasClass("active")) {
		$("#maincontainer").css('left', '');
	  }
	  else {
		$("#maincontainer").css('left', '280px');
	  }
	});
})(jQuery);
