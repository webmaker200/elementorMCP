<?php
/**
 * Clear page caches when a testimonial changes.
 *
 * @package MedCare_Testimonials
 */

defined( 'ABSPATH' ) || exit;

add_action( 'save_post_mc_testimonial', 'mc_tst_clear_cache', 20, 2 );
add_action( 'trashed_post', 'mc_tst_maybe_clear_cache' );
add_action( 'untrashed_post', 'mc_tst_maybe_clear_cache' );
add_action( 'deleted_post', 'mc_tst_maybe_clear_cache' );

/**
 * Save handler.
 *
 * @param int     $post_id Post ID.
 * @param WP_Post $post    Post.
 */
function mc_tst_clear_cache( $post_id, $post ) {
	if ( wp_is_post_revision( $post_id ) || wp_is_post_autosave( $post_id ) || 'auto-draft' === $post->post_status ) {
		return;
	}
	mc_tst_flush();
}

/**
 * Trash/untrash/delete handler.
 *
 * @param int $post_id Post ID.
 */
function mc_tst_maybe_clear_cache( $post_id ) {
	if ( 'mc_testimonial' === get_post_type( $post_id ) ) {
		mc_tst_flush();
	}
}

/**
 * Purge WP Rocket when it is active. Other hosts/caches can hook mc_testimonials_flush_cache.
 */
function mc_tst_flush() {
	if ( function_exists( 'rocket_clean_domain' ) ) {
		rocket_clean_domain();
	}
	do_action( 'mc_testimonials_flush_cache' );
}
