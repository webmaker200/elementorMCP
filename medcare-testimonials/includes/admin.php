<?php
/**
 * Admin list columns: photo and order, sorted by order.
 *
 * @package MedCare_Testimonials
 */

defined( 'ABSPATH' ) || exit;

add_filter( 'manage_mc_testimonial_posts_columns', 'mc_tst_columns' );
add_action( 'manage_mc_testimonial_posts_custom_column', 'mc_tst_column', 10, 2 );
add_filter( 'manage_edit-mc_testimonial_sortable_columns', 'mc_tst_sortable' );
add_action( 'pre_get_posts', 'mc_tst_admin_order' );

/**
 * Columns.
 *
 * @param array $columns Columns.
 * @return array
 */
function mc_tst_columns( $columns ) {
	$out = array();
	foreach ( $columns as $key => $label ) {
		if ( 'title' === $key ) {
			$out['mc_photo'] = __( 'Photo', 'medcare-testimonials' );
			$out[ $key ]     = __( 'Name', 'medcare-testimonials' );
			$out['mc_order'] = __( 'Order', 'medcare-testimonials' );
			continue;
		}
		$out[ $key ] = $label;
	}
	return $out;
}

/**
 * Column output.
 *
 * @param string $column  Column.
 * @param int    $post_id Post ID.
 */
function mc_tst_column( $column, $post_id ) {
	if ( 'mc_photo' === $column ) {
		$image = (int) get_post_meta( $post_id, 'mc_image', true );
		if ( $image ) {
			echo wp_get_attachment_image( $image, array( 40, 51 ), false, array( 'style' => 'width:40px;height:auto' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		}
	} elseif ( 'mc_order' === $column ) {
		echo esc_html( (string) get_post_field( 'menu_order', $post_id ) );
	}
}

/**
 * Sortable columns.
 *
 * @param array $columns Columns.
 * @return array
 */
function mc_tst_sortable( $columns ) {
	$columns['mc_order'] = 'menu_order';
	return $columns;
}

/**
 * Default admin order = front-end order.
 *
 * @param WP_Query $query Query.
 */
function mc_tst_admin_order( $query ) {
	if ( is_admin() && $query->is_main_query() && 'mc_testimonial' === $query->get( 'post_type' ) && ! $query->get( 'orderby' ) ) {
		$query->set(
			'orderby',
			array(
				'menu_order' => 'ASC',
				'date'       => 'DESC',
			)
		);
	}
}
