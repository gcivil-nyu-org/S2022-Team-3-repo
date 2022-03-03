(function($) {

	var	$window = $(window),
		$body = $('body'),
		$nav = $('#nav');

		// Breakpoints.
		breakpoints({
			xlarge:  [ '1281px',  '1680px' ],
			large:   [ '981px',   '1280px' ],
			medium:  [ '737px',   '980px'  ],
			small:   [ '361px',   '736px'  ],
			xsmall:  [ null,      '360px'  ]
		});

		$(window).scroll(function() {
			scrollFunction();
		});
				
		$('#scrollToTopBtn').hide();

		function scrollFunction() {
			if (document.documentElement.scrollTop > 50) {
				$('#scrollToTopBtn').show();
			} else {
				$('#scrollToTopBtn').hide();
			}
		}

		$('#scrollToTopBtn').click(function() {
			$('html, body').animate({scrollTop : 0},700);
		});

		// Nav.

		// Title Bar.
			$(
				'<div id="titleBar">' +
					'<a href="#navPanel" class="toggle"></a>' +
					'<span class="title">' + $('#logo').html() + '</span>' +
				'</div>'
			)
				.appendTo($body);

		// Panel.
			$(
				'<div id="navPanel">' +
					'<nav>' +
						$('#nav').navList() +
					'</nav>' +
				'</div>'
			)
				.appendTo($body)
				.panel({
					delay: 500,
					hideOnClick: true,
					hideOnSwipe: true,
					resetScroll: true,
					resetForms: true,
					side: 'left',
					target: $body,
					visibleClass: 'navPanel-visible'
				});

})(jQuery);