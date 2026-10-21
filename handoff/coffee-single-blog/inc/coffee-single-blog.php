<?php
/**
 * Coffee Fix DXB – single blog post helpers.
 *
 * Load from your (child) theme's functions.php:
 *     require_once get_stylesheet_directory() . '/inc/coffee-single-blog.php';
 *
 * Everything inside the post (title, excerpt, banner, content, table of
 * contents, tags, author, date, reading time, related posts) is pulled from
 * WordPress automatically. Only the brand/contact text below is fixed – edit
 * it here once, or change it with the `cfb_settings` filter.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Brand / CTA settings used by the template.
 */
function cfb_settings() {
	$phone = '+971568434032';

	return apply_filters(
		'cfb_settings',
		array(
			'phone'            => $phone,
			'phone_label'      => '+971 56 843 4032',
			'whatsapp_url'     => 'https://wa.me/971568434032?text=' . rawurlencode( 'Hi Coffee Fix DXB, I need help with my coffee machine.' ),
			'author_tagline'   => 'On-site coffee machine repair across Dubai', // Used when the author has no bio.
			'words_per_minute' => 200,

			// Sidebar card.
			'side_eyebrow'     => 'Machine still cold?',
			'side_title'       => 'Free diagnosis, clear price',
			'side_text'        => 'A technician comes to you anywhere in Dubai, finds the real fault and tells you the price before any work starts.',
			'side_whatsapp'    => 'WhatsApp a technician',

			// Related posts.
			'related_eyebrow'  => 'Keep reading',
			'related_title'    => 'Related articles',
			'related_all'      => 'View all articles &rarr;',
			'related_count'    => 3,

			// Bottom contact band.
			'contact_eyebrow'  => 'Still stuck?',
			'contact_title'    => 'Let a technician take a look',
			'contact_text'     => 'Tell us what your machine is doing and where you are in Dubai. Diagnosis is free, and you get a clear price before any work starts.',
			'contact_whatsapp' => 'Book a repair on WhatsApp',
		)
	);
}

/**
 * Styles + font, only on single blog posts.
 */
function cfb_enqueue_assets() {
	if ( ! is_singular( 'post' ) ) {
		return;
	}

	$file = get_stylesheet_directory() . '/assets/css/coffee-single-blog.css';

	wp_enqueue_style(
		'cfb-font',
		'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap',
		array(),
		null
	);
	wp_enqueue_style(
		'cfb-single-blog',
		get_stylesheet_directory_uri() . '/assets/css/coffee-single-blog.css',
		array( 'cfb-font' ),
		file_exists( $file ) ? filemtime( $file ) : null
	);
}
add_action( 'wp_enqueue_scripts', 'cfb_enqueue_assets', 20 );

/**
 * URL of the blog listing (Settings → Reading → Posts page), or home.
 */
function cfb_blog_url() {
	$page_id = (int) get_option( 'page_for_posts' );

	return $page_id ? get_permalink( $page_id ) : home_url( '/' );
}

/**
 * Primary category (Yoast / Rank Math primary when set, else the first one).
 */
function cfb_primary_category( $post_id = null ) {
	$post_id = $post_id ? $post_id : get_the_ID();
	$primary = 0;

	if ( function_exists( 'yoast_get_primary_term_id' ) ) {
		$primary = (int) yoast_get_primary_term_id( 'category', $post_id );
	}
	if ( ! $primary ) {
		$primary = (int) get_post_meta( $post_id, 'rank_math_primary_category', true );
	}
	if ( $primary ) {
		$term = get_term( $primary, 'category' );
		if ( $term && ! is_wp_error( $term ) ) {
			return $term;
		}
	}

	$cats = get_the_category( $post_id );

	return $cats ? $cats[0] : null;
}

/**
 * Reading time in minutes. A custom field `cfb_reading_time` overrides it.
 */
function cfb_reading_time( $post_id = null ) {
	$post_id = $post_id ? $post_id : get_the_ID();
	$manual  = (int) get_post_meta( $post_id, 'cfb_reading_time', true );

	if ( $manual > 0 ) {
		return $manual;
	}

	$text  = wp_strip_all_tags( strip_shortcodes( get_post_field( 'post_content', $post_id ) ) );
	$words = count( preg_split( '/\s+/u', trim( $text ), -1, PREG_SPLIT_NO_EMPTY ) );

	return max( 1, (int) ceil( $words / max( 1, (int) cfb_settings()['words_per_minute'] ) ) );
}

/**
 * Lead paragraph under the title: the manual excerpt, else the start of the post.
 */
function cfb_lead( $post_id = null, $words = 32 ) {
	$post_id = $post_id ? $post_id : get_the_ID();

	if ( has_excerpt( $post_id ) ) {
		return get_the_excerpt( $post_id );
	}

	return wp_trim_words( strip_shortcodes( get_post_field( 'post_content', $post_id ) ), $words, '&hellip;' );
}

/**
 * Gives every H2 in the content an id and returns the list for the
 * "In this article" box.
 *
 * @return array { html: string, toc: array<array{id,label}> }
 */
function cfb_prepare_content( $html ) {
	$toc  = array();
	$used = array();

	$html = preg_replace_callback(
		'#<h2(\s[^>]*)?>(.*?)</h2>#is',
		function ( $m ) use ( &$toc, &$used ) {
			$attrs = isset( $m[1] ) ? $m[1] : '';
			$text  = trim( wp_strip_all_tags( $m[2] ) );

			if ( preg_match( '/\sid=["\']([^"\']+)["\']/i', $attrs, $id ) ) {
				$slug = $id[1];
			} else {
				$base = sanitize_title( $text );
				$base = $base ? $base : 'section';
				$slug = $base;
				$n    = 2;
				while ( isset( $used[ $slug ] ) ) {
					$slug = $base . '-' . $n++;
				}
				$attrs .= ' id="' . esc_attr( $slug ) . '"';
			}
			$used[ $slug ] = true;

			// "1. Start with the simple checks" → "Start with the simple checks".
			$label = preg_replace( '/^\d+[\.\)]\s*/', '', $text );
			$toc[] = array(
				'id'    => $slug,
				'label' => $label,
			);

			return '<h2' . $attrs . '>' . $m[2] . '</h2>';
		},
		$html
	);

	return array(
		'html' => $html,
		'toc'  => $toc,
	);
}

/**
 * Related posts: same categories first, topped up with the latest posts.
 */
function cfb_related_posts( $post_id = null, $count = 3 ) {
	$post_id = $post_id ? $post_id : get_the_ID();
	$cats    = wp_get_post_categories( $post_id );
	$posts   = array();

	if ( $cats ) {
		$posts = get_posts(
			array(
				'post_type'           => 'post',
				'posts_per_page'      => $count,
				'post__not_in'        => array( $post_id ),
				'category__in'        => $cats,
				'ignore_sticky_posts' => true,
				'no_found_rows'       => true,
			)
		);
	}

	if ( count( $posts ) < $count ) {
		$exclude = array_merge( array( $post_id ), wp_list_pluck( $posts, 'ID' ) );
		$posts   = array_merge(
			$posts,
			get_posts(
				array(
					'post_type'           => 'post',
					'posts_per_page'      => $count - count( $posts ),
					'post__not_in'        => $exclude,
					'ignore_sticky_posts' => true,
					'no_found_rows'       => true,
				)
			)
		);
	}

	return $posts;
}

/**
 * Inline SVG icons used by the design (Font Awesome 5 solid paths).
 */
function cfb_icon( $name ) {
	$icons = array(
		'wrench'      => array( '0 0 512 512', 'M501.1 395.7L384 278.6c-23.1-23.1-57.6-27.6-85.4-13.9L192 158.1V96L64 0 0 64l96 128h62.1l106.6 106.6c-13.6 27.8-9.2 62.3 13.9 85.4l117.1 117.1c14.6 14.6 38.2 14.6 52.7 0l52.7-52.7c14.5-14.6 14.5-38.2 0-52.7zM331.7 225c28.3 0 54.9 11 74.9 31l19.4 19.4c15.8-6.9 30.8-16.5 43.8-29.5 37.1-37.1 49.7-89.3 37.9-136.7-2.2-9-13.5-12.1-20.1-5.5l-74.4 74.4-67.9-11.3L334 98.9l74.4-74.4c6.6-6.6 3.4-17.9-5.7-20.2-47.4-11.7-99.6.9-136.6 37.9-28.5 28.5-41.9 66.1-41.2 103.6l82.1 82.1c8.1-1.9 16.5-2.9 24.7-2.9zm-103.9 82l-56.7-56.7L18.7 402.8c-25 25-25 65.5 0 90.5s65.5 25 90.5 0l123.6-123.6c-7.6-19.9-9.9-41.6-5-62.7zM64 472c-13.2 0-24-10.8-24-24 0-13.3 10.7-24 24-24s24 10.7 24 24c0 13.2-10.7 24-24 24z' ),
		'thermometer' => array( '0 0 256 512', 'M192 384c0 35.346-28.654 64-64 64s-64-28.654-64-64c0-23.685 12.876-44.349 32-55.417V224c0-17.673 14.327-32 32-32s32 14.327 32 32v104.583c19.124 11.068 32 31.732 32 55.417zm32-84.653c19.912 22.563 32 52.194 32 84.653 0 70.696-57.303 128-128 128-.299 0-.609-.001-.909-.003C56.789 511.509-.357 453.636.002 383.333.166 351.135 12.225 321.755 32 299.347V96c0-53.019 42.981-96 96-96s96 42.981 96 96v203.347zM208 384c0-34.339-19.37-52.19-32-66.502V96c0-26.467-21.533-48-48-48S80 69.533 80 96v221.498c-12.732 14.428-31.825 32.1-31.999 66.08-.224 43.876 35.563 80.116 79.423 80.42L128 464c44.112 0 80-35.888 80-80z' ),
		'tint'        => array( '0 0 352 512', 'M205.22 22.09c-7.94-28.78-49.44-30.12-58.44 0C100.01 179.85 0 222.72 0 333.91 0 432.35 78.72 512 176 512s176-79.65 176-178.09c0-111.75-99.79-153.34-146.78-311.82zM176 448c-61.75 0-112-50.25-112-112 0-8.84 7.16-16 16-16s16 7.16 16 16c0 44.11 35.89 80 80 80 8.84 0 16 7.16 16 16s-7.16 16-16 16z' ),
		'search'      => array( '0 0 512 512', 'M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z' ),
	);

	if ( ! isset( $icons[ $name ] ) ) {
		return '';
	}

	return sprintf(
		'<svg xmlns="http://www.w3.org/2000/svg" viewBox="%1$s" fill="currentColor" aria-hidden="true" focusable="false"><path d="%2$s"></path></svg>',
		esc_attr( $icons[ $name ][0] ),
		esc_attr( $icons[ $name ][1] )
	);
}
