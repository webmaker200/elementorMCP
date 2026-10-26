<?php
/**
 * One-time import of 5 testimonials from the homepage carousel (template 388878),
 * copied verbatim. Runs on activation only if no testimonials exist yet.
 *
 * @package MedCare_Testimonials
 */

defined( 'ABSPATH' ) || exit;

/**
 * Initial content, in carousel order.
 *
 * @return array[]
 */
function mc_tst_seed_data() {
	return array(
		array(
			'name'      => 'Dr. Jose Correa',
			'headline'  => 'Recommended',
			'quote'     => 'I highly recommend MedCare MSO if you are looking for help with your billing and gain some freedom to see more patients or manage your business.',
			'role'      => 'Practice Owner',
			'org'       => 'TXEC',
			'image'     => 401937,
		),
		array(
			'name'      => 'Shaunna Mock',
			'headline'  => 'Outstanding',
			'quote'     => 'MedCare MSO has been an excellent organization to work with, I highly recommend them for their quality of service and commitment to excellence.',
			'role'      => 'Back Office Manager',
			'org'       => 'STST',
			'image'     => 401412,
		),
		array(
			'name'      => 'Max Owens',
			'headline'  => 'Talented',
			'quote'     => 'We are definitely impressed by the Team’s performance. I worked with a lot of different folks from all over the world on different business transactions, and Mark is truly a top notch talent!',
			'role'      => 'Director of Corporate Development',
			'org'       => 'SC & SF',
			'image'     => 399532,
		),
		array(
			'name'      => 'Kelly Ballou',
			'headline'  => 'Exceptional',
			'quote'     => 'MedCare MSO’s exceptional communication and expertise elevated our RCM experience and my bank accounts!',
			'role'      => 'Owner',
			'org'       => 'R.D.',
			'image'     => 397918,
		),
		array(
			'name'      => 'Bret',
			'headline'  => 'Communicative',
			'quote'     => 'MedCare MSO did a great job with our billing and helping clean up old AR. Regular updates and good communication were very appreciated.',
			'role'      => 'Co-Owner',
			'org'       => 'PCP',
			'image'     => 396539,
		),
	);
}

/**
 * Create the testimonial posts once.
 */
function mc_tst_seed() {
	if ( get_option( 'mc_tst_seeded' ) ) {
		return;
	}
	$existing = get_posts(
		array(
			'post_type'      => 'mc_testimonial',
			'post_status'    => 'any',
			'posts_per_page' => 1,
			'fields'         => 'ids',
		)
	);
	if ( $existing ) {
		update_option( 'mc_tst_seeded', 1, false );
		return;
	}

	$fields = array(
		'mc_headline'     => 'headline',
		'mc_quote'        => 'quote',
		'mc_role'         => 'role',
		'mc_organization' => 'org',
		'mc_image'        => 'image',
	);

	foreach ( mc_tst_seed_data() as $order => $item ) {
		$post_id = wp_insert_post(
			array(
				'post_type'   => 'mc_testimonial',
				'post_status' => 'publish',
				'post_title'  => $item['name'],
				'menu_order'  => $order,
			),
			true
		);
		if ( is_wp_error( $post_id ) ) {
			continue;
		}
		foreach ( $fields as $meta_key => $source ) {
			$value = $item[ $source ];
			if ( '' === $value || 0 === $value ) {
				continue;
			}
			// Same storage ACF uses: value + field-key reference.
			update_post_meta( $post_id, $meta_key, $value );
			update_post_meta( $post_id, '_' . $meta_key, 'field_' . $meta_key );
		}
	}
	update_option( 'mc_tst_seeded', 1, false );
}
