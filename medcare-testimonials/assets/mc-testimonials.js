/**
 * MedCare Testimonials: two synced, infinite Swiper tracks (photos + quotes).
 * Uses the Swiper 8 bundle Elementor registers as "swiper". Without it the
 * section stays in its static first-slide layout, which is identical to the
 * pre-JS render.
 */
( function () {
	'use strict';

	var reduceMotion = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;

	// Narrowest photo slot in the CSS (tablet: 165px slide + 10px gap).
	var MIN_SLOT = 175;
	// Widest photo slot (desktop: 312px slide + 10px gap).
	var MAX_SLOT = 322;

	function init( section ) {
		if ( section.mcTst || typeof window.Swiper !== 'function' ) {
			return;
		}
		section.mcTst = true;

		var mediaEl = section.querySelector( '.mc-tst__media' );
		var quotesEl = section.querySelector( '.mc-tst__quotes' );
		var photoTrack = mediaEl.querySelector( '.mc-tst__track' );
		var dots = section.querySelectorAll( '.mc-tst__dot' );
		var count = section.querySelectorAll( '.mc-tst__card' ).length;
		var speed = reduceMotion ? 0 : 1000;
		var syncing = false;

		// Infinite loop at every width: with few testimonials, repeat the photo set
		// until one pass is wider than any screen, so the loop never shows a gap.
		var originals = Array.prototype.slice.call( photoTrack.children );
		var widest = Math.max( window.screen ? window.screen.width : 0, window.innerWidth, mediaEl.clientWidth ) + MAX_SLOT;
		var sets = Math.max( 1, Math.ceil( widest / ( count * MIN_SLOT ) ) );
		for ( var s = 1; s < sets; s++ ) {
			originals.forEach( function ( el ) {
				var copy = el.cloneNode( true );
				copy.classList.remove( 'is-active' );
				photoTrack.appendChild( copy );
			} );
		}
		var total = count * sets;

		var photos = new window.Swiper( mediaEl, {
			wrapperClass: 'mc-tst__track',
			slideClass: 'mc-tst__slide',
			loop: true,
			loopedSlides: total,
			slidesPerView: 'auto',
			spaceBetween: 0, // The 10px gap is a CSS margin, so the static layout and Swiper's grid match.
			speed: speed,
			grabCursor: true,
			watchSlidesProgress: true,
			autoplay: reduceMotion ? false : { delay: 5000, disableOnInteraction: false }
		} );

		var quotes = new window.Swiper( quotesEl, {
			wrapperClass: 'mc-tst__track',
			slideClass: 'mc-tst__slide',
			loop: true,
			loopedSlides: count,
			slidesPerView: 1,
			spaceBetween: 30,
			speed: speed,
			grabCursor: true,
			a11y: {
				enabled: true,
				containerMessage: section.querySelector( '.mc-tst__title' ).textContent,
				slideLabelMessage: '{{index}} / {{slidesLength}}'
			}
		} );

		// Testimonial number (0..count-1) currently shown.
		function current() {
			return photos.realIndex % count;
		}

		// Move a track to testimonial `target`. One step uses next/prev so the
		// last -> first wrap keeps moving forward; bigger jumps go forward too.
		function move( swiper, size, target ) {
			var here = swiper.realIndex;
			if ( here % count === target ) {
				return;
			}
			if ( ( here + 1 ) % count === target ) {
				swiper.slideNext();
			} else if ( ( here - 1 + count ) % count === target ) {
				swiper.slidePrev();
			} else {
				swiper.slideToLoop( ( here + ( ( target - ( here % count ) + count ) % count ) ) % size );
			}
		}

		function update() {
			var index = current();
			// Enlarge the active photo (Swiper's slide index; loop duplicates share it).
			section.querySelectorAll( '.mc-tst__photo' ).forEach( function ( el ) {
				el.classList.toggle( 'is-active', +el.getAttribute( 'data-swiper-slide-index' ) === photos.realIndex );
			} );
			dots.forEach( function ( dot, i ) {
				if ( i === index ) {
					dot.setAttribute( 'aria-current', 'true' );
				} else {
					dot.removeAttribute( 'aria-current' );
				}
			} );
			// Keep links in off-screen (and duplicated) quote slides out of the tab order.
			quotes.slides.forEach( function ( el, i ) {
				el.inert = i !== quotes.activeIndex;
			} );
		}

		// Whichever track changes (arrows, dots, swipe, autoplay), the other follows at once.
		photos.on( 'slideChange', function () {
			update();
			if ( ! syncing ) {
				syncing = true;
				move( quotes, count, current() );
				syncing = false;
			}
		} );
		quotes.on( 'slideChange', function () {
			if ( ! syncing ) {
				syncing = true;
				move( photos, total, quotes.realIndex );
				syncing = false;
			}
		} );
		quotes.on( 'slideChangeTransitionEnd', update );

		section.querySelector( '.mc-tst__next' ).addEventListener( 'click', function () {
			photos.slideNext();
		} );
		section.querySelector( '.mc-tst__prev' ).addEventListener( 'click', function () {
			photos.slidePrev();
		} );
		dots.forEach( function ( dot ) {
			dot.addEventListener( 'click', function () {
				move( photos, total, +dot.getAttribute( 'data-index' ) );
			} );
		} );

		// Pause autoplay on hover and on keyboard focus.
		if ( photos.params.autoplay && photos.params.autoplay.enabled ) {
			var hovered = false;
			var focused = false;
			var live = quotesEl.querySelector( '.mc-tst__track' );
			var sync = function () {
				if ( hovered || focused ) {
					photos.autoplay.stop();
					live.setAttribute( 'aria-live', 'polite' );
				} else {
					photos.autoplay.start();
					live.setAttribute( 'aria-live', 'off' );
				}
			};
			section.addEventListener( 'mouseenter', function () {
				hovered = true;
				sync();
			} );
			section.addEventListener( 'mouseleave', function () {
				hovered = false;
				sync();
			} );
			// Keyboard focus only: mouse clicks also focus buttons but should not stop autoplay.
			section.addEventListener( 'focusin', function ( e ) {
				var keyboard = true;
				try {
					keyboard = e.target.matches( ':focus-visible' );
				} catch ( err ) {}
				if ( keyboard ) {
					focused = true;
					sync();
				}
			} );
			section.addEventListener( 'focusout', function ( e ) {
				if ( ! section.contains( e.relatedTarget ) ) {
					focused = false;
					sync();
				}
			} );
			live.setAttribute( 'aria-live', 'off' );
		}

		update();
	}

	function boot() {
		document.querySelectorAll( '.mc-tst[data-count]' ).forEach( function ( section ) {
			if ( +section.getAttribute( 'data-count' ) > 1 ) {
				init( section );
			}
		} );
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', boot );
	} else {
		boot();
	}
}() );
