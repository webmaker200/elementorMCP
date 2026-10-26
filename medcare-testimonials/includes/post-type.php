<?php
/**
 * Testimonial post type.
 *
 * @package MedCare_Testimonials
 */

defined( 'ABSPATH' ) || exit;

add_action( 'init', 'mc_tst_register_post_type' );

/**
 * Register the mc_testimonial post type: admin-only, no front-end URLs.
 */
function mc_tst_register_post_type() {
	register_post_type(
		'mc_testimonial',
		array(
			'labels'              => array(
				'name'               => __( 'Testimonials', 'medcare-testimonials' ),
				'singular_name'      => __( 'Testimonial', 'medcare-testimonials' ),
				'menu_name'          => __( 'Testimonials', 'medcare-testimonials' ),
				'add_new_item'       => __( 'Add New Testimonial', 'medcare-testimonials' ),
				'edit_item'          => __( 'Edit Testimonial', 'medcare-testimonials' ),
				'new_item'           => __( 'New Testimonial', 'medcare-testimonials' ),
				'search_items'       => __( 'Search Testimonials', 'medcare-testimonials' ),
				'not_found'          => __( 'No testimonials found.', 'medcare-testimonials' ),
				'not_found_in_trash' => __( 'No testimonials found in Trash.', 'medcare-testimonials' ),
			),
			'public'              => false,
			'publicly_queryable'  => false,
			'exclude_from_search' => true,
			'show_ui'             => true,
			'show_in_menu'        => true,
			'show_in_nav_menus'   => false,
			'show_in_admin_bar'   => false,
			'show_in_rest'        => false,
			'has_archive'         => false,
			'rewrite'             => false,
			'query_var'           => false,
			'menu_icon'           => 'dashicons-format-quote',
			'supports'            => array( 'title', 'page-attributes' ),
			'capability_type'     => 'post',
			'map_meta_cap'        => true,
		)
	);
}

// Keep the post type out of sitemaps (core and Yoast), even though it is not public.
add_filter(
	'wp_sitemaps_post_types',
	static function ( $post_types ) {
		unset( $post_types['mc_testimonial'] );
		return $post_types;
	}
);
add_filter(
	'wpseo_sitemap_exclude_post_type',
	static function ( $excluded, $post_type ) {
		return 'mc_testimonial' === $post_type ? true : $excluded;
	},
	10,
	2
);

add_filter( 'enter_title_here', 'mc_tst_title_placeholder', 10, 2 );

/**
 * Make it clear that the title is the person's name.
 *
 * @param string  $text Placeholder.
 * @param WP_Post $post Post being edited.
 * @return string
 */
function mc_tst_title_placeholder( $text, $post ) {
	return 'mc_testimonial' === $post->post_type ? __( "Person's name", 'medcare-testimonials' ) : $text;
}
