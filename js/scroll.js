$(document).ready(function() {
	$(this).scrollTop(0);


	$(".section-link").on('click', function(event) {
	    event.preventDefault();

	    var target = this.hash;
	    var $target = $(target);
		  var x = $(window).width();

			$('html, body').stop().animate( {
		      'scrollTop': $target.offset().top - 60
		  }, 1200, 'swing');
	});

	$(window).scroll(function() {
		var height = $(window).scrollTop();

		if (height >= 300) {
	    $("#header-bar").fadeIn(200);
	  } else {
	    $("#header-bar").fadeOut(200);
	  }
	});
});
