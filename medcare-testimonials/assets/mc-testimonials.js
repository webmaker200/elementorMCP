/**
 * MedCare Testimonials: two synced Swiper tracks (photos + quotes).
 * Uses the Swiper 8 bundle Elementor registers as "swiper". Without it the
 * section stays in its static first-slide layout, which is identical to the
 * pre-JS render.
 */
( function () {
	'use strict';

	var reduceMotion = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;

	function init( section ) {
		if ( section.mcTst || typeof window.Swiper !== 'function' ) {
			return;
		}
		section.mcTst = true;

		var mediaEl = section.querySelector( '.mc-tst__media' );
		var quotesEl = section.querySelector( '.mc-tst__quotes' );
		var dots = section.querySelectorAll( '.mc-tst__dot' );
		var count = section.querySelectorAll( '.mc-tst__card' ).length;
		var speed = reduceMotion ? 0 : 1000;
		var syncing = false;

		// Loop only when there are more items than the photo track can show at once.
		var slot = section.querySelector( '.mc-tst__photo' ).getBoundingClientRect().width + 10;
		var loop = count > Math.ceil( mediaEl.clientWidth / slot );

		var common = {
			wrapperClass: 'mc-tst__track',
			slideClass: 'mc-tst__slide',
			loop: loop,
			loopedSlides: count,
			speed: speed,
			grabCursor: true,
			watchSlidesProgress: true
		};

		var autoplay = { delay: 5000, disableOnInteraction: false };

		var photos = new window.Swiper( mediaEl, Object.assign( {}, common, {
			slidesPerView: 'auto',
			spaceBetween: 0, // The 10px gap is a CSS margin, so the static layout and Swiper's grid match.
			// When every photo already fits, the photo track cannot move; the quote track autoplays instead.
			autoplay: reduceMotion || ! loop ? false : autoplay
		} ) );

		var quotes = new window.Swiper( quotesEl, Object.assign( {}, common, {
			slidesPerView: 1,
			spaceBetween: 30,
			rewind: ! loop,
			autoplay: reduceMotion || loop ? false : autoplay,
			autoHeight: false,
			a11y: {
				enabled: true,
				containerMessage: section.querySelector( '.mc-tst__title' ).textContent,
				slideLabelMessage: '{{index}} / {{slidesLength}}'
			}
		} ) );

		// Move the follower one step in the same direction when possible, so the
		// last -> first wrap animates forward instead of rewinding.
		function follow( follower, target ) {
			var current = follower.realIndex;
			if ( current === target ) {
				return;
			}
			if ( ! loop ) {
				follower.slideTo( target );
			} else if ( target === ( current + 1 ) % count ) {
				follower.slideNext();
			} else if ( target === ( current - 1 + count ) % count ) {
				follower.slidePrev();
			} else {
				follower.slideToLoop( target );
			}
		}

		// The photo track leads while looping; otherwise it is locked and the quote track leads.
		var lead = loop ? photos : quotes;

		function update() {
			var index = lead.realIndex;
			section.querySelectorAll( '.mc-tst__photo' ).forEach( function ( el ) {
				el.classList.toggle( 'is-active', +el.getAttribute( 'data-index' ) === index );
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

		function link( leader, other ) {
			leader.on( 'slideChange', function () {
				if ( syncing ) {
					return;
				}
				syncing = true;
				follow( other, leader.realIndex );
				syncing = false;
			} );
		}
		link( photos, quotes );
		link( quotes, photos );
		lead.on( 'slideChange', update );
		quotes.on( 'slideChangeTransitionEnd', update );

		function go( index ) {
			if ( loop ) {
				photos.slideToLoop( index );
			} else {
				quotes.slideTo( index );
			}
		}

		section.querySelector( '.mc-tst__next' ).addEventListener( 'click', function () {
			lead.slideNext();
		} );
		section.querySelector( '.mc-tst__prev' ).addEventListener( 'click', function () {
			lead.slidePrev();
		} );
		dots.forEach( function ( dot ) {
			dot.addEventListener( 'click', function () {
				go( +dot.getAttribute( 'data-index' ) );
			} );
		} );

		// Pause autoplay on hover and while anything in the section has focus.
		var auto = loop ? photos : quotes;
		if ( auto.params.autoplay && auto.params.autoplay.enabled ) {
			var hovered = false;
			var focused = false;
			var live = quotesEl.querySelector( '.mc-tst__track' );
			var sync = function () {
				if ( hovered || focused ) {
					auto.autoplay.stop();
					live.setAttribute( 'aria-live', 'polite' );
				} else {
					auto.autoplay.start();
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
