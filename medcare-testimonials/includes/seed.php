<?php
/**
 * One-time import of the testimonials that were on the homepage (template 388878),
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
			'logo'      => 0,
			'cta_type'  => 'popup',
			'popup_id'  => 401929,
			'video_url' => '',
		),
		array(
			'name'      => 'Shaunna Mock',
			'headline'  => 'Outstanding',
			'quote'     => 'MedCare MSO has been an excellent organization to work with, I highly recommend them for their quality of service and commitment to excellence.',
			'role'      => 'Back Office Manager',
			'org'       => 'STST',
			'image'     => 401412,
			'logo'      => 0,
			'cta_type'  => 'popup',
			'popup_id'  => 401419,
			'video_url' => '',
		),
		array(
			'name'      => 'Max Owens',
			'headline'  => 'Talented',
			'quote'     => 'We are definitely impressed by the Team’s performance. I worked with a lot of different folks from all over the world on different business transactions, and Mark is truly a top notch talent!',
			'role'      => 'Director of Corporate Development',
			'org'       => 'SC & SF',
			'image'     => 399532,
			'logo'      => 0,
			'cta_type'  => 'popup',
			'popup_id'  => 399519,
			'video_url' => '',
		),
		array(
			'name'      => 'Kelly Ballou',
			'headline'  => 'Exceptional',
			'quote'     => 'MedCare MSO’s exceptional communication and expertise elevated our RCM experience and my bank accounts!',
			'role'      => 'Owner',
			'org'       => 'R.D.',
			'image'     => 397918,
			'logo'      => 0,
			'cta_type'  => 'popup',
			'popup_id'  => 397920,
			'video_url' => '',
		),
		array(
			'name'      => 'Bret',
			'headline'  => 'Communicative',
			'quote'     => 'MedCare MSO did a great job with our billing and helping clean up old AR. Regular updates and good communication were very appreciated.',
			'role'      => 'Co-Owner',
			'org'       => 'PCP',
			'image'     => 396539,
			'logo'      => 0,
			'cta_type'  => 'popup',
			'popup_id'  => 396530,
			'video_url' => '',
		),
		array(
			'name'      => 'JOSHUA ARANT',
			'headline'  => 'Great',
			'quote'     => 'Our experience with MedCare MSO is great. They help us to increase our revenue with their quality medical billing and customer support services. Always recommend them to others.',
			'role'      => 'Chief Operating Officer',
			'org'       => 'MAKO MEDICAL LABORATORIES',
			'image'     => 398177,
			'logo'      => 1040,
			'cta_type'  => 'video',
			'popup_id'  => 0,
			'video_url' => 'https://player.vimeo.com/video/428248198?h=dce96a3d73#t=',
		),
		array(
			'name'      => 'SHOBHA SOLOMON',
			'headline'  => 'Efficient',
			'quote'     => 'I am very thankful to MedCare MSO because they rectified all the mistakes which were done by my previous medical billing partner. They are so fast and efficient.',
			'role'      => 'Chief Executive Officer',
			'org'       => 'CARE NOW CLINIC',
			'image'     => 383594,
			'logo'      => 380514,
			'cta_type'  => 'video',
			'popup_id'  => 0,
			'video_url' => 'https://player.vimeo.com/video/516346500?h=dce96a3d73#t=',
		),
		array(
			'name'      => 'JAMES BERG',
			'headline'  => 'Outstanding',
			'quote'     => 'MedCare MSO has been and continues to be critical to the success of Ion Diagnostics. As our medical billing company, they consistently meet our needs for compliance and dedicated, responsive client service. They excel in revenue cycle management and truly feel like a partner.',
			'role'      => 'Chief Operations Officer',
			'org'       => 'ION DIAGNOSTICS',
			'image'     => 383595,
			'logo'      => 383574,
			'cta_type'  => 'video',
			'popup_id'  => 0,
			'video_url' => 'https://player.vimeo.com/video/757324121?h=dce96a3d73#t=',
		),
		array(
			'name'      => 'Doctor Godfred Mensah',
			'headline'  => 'Responsive',
			'quote'     => 'MedCare MSO, as our medical billing company, has reduced our claim denials by up to 20% and resolved all of our billing challenges, including prior authorization and credentialing. We have regularly scheduled weekly meetings with them, and they have been very responsive and courteous during the calls',
			'role'      => 'Co-Founder',
			'org'       => 'AW Care',
			'image'     => 388835,
			'logo'      => 0,
			'cta_type'  => 'video',
			'popup_id'  => 0,
			'video_url' => 'https://medcaredemo.online/medcare/wp-content/uploads/2025/03/AW-care.mp4',
		),
		array(
			'name'      => 'Dr. Chess',
			'headline'  => 'Efficient',
			'quote'     => 'Working with MedCare MSO has been a game-changer for my practice. Their expertise in medical billing, AR management, and coding has significantly streamlined our revenue cycle, reduced claim denials, and improved cash flow. The team is proactive, detail-oriented, and always available to address my concerns.',
			'role'      => 'Practice Owner',
			'org'       => 'F&A Clinic',
			'image'     => 391797,
			'logo'      => 0,
			'cta_type'  => 'popup',
			'popup_id'  => 383332,
			'video_url' => '',
		),
		array(
			'name'      => 'Daniel',
			'headline'  => 'Excellent',
			'quote'     => 'We have experienced tremendous improvements within our billing and claims department that we have entrusted MedCare MSO to manage.',
			'role'      => 'President/CEO',
			'org'       => 'RLT',
			'image'     => 393478,
			'logo'      => 0,
			'cta_type'  => 'popup',
			'popup_id'  => 393492,
			'video_url' => '',
		),
		array(
			'name'      => 'Dr. Neufeld',
			'headline'  => 'Impressive',
			'quote'     => 'I am impressed with MedCare MSO’s promptness to respond to any inquiries, with the time they dedicate to reviewing each one of the cases.',
			'role'      => 'Practice Owner/FBH',
			'org'       => '',
			'image'     => 394793,
			'logo'      => 0,
			'cta_type'  => 'popup',
			'popup_id'  => 394798,
			'video_url' => '',
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
		'mc_logo'         => 'logo',
		'mc_cta_type'     => 'cta_type',
		'mc_popup_id'     => 'popup_id',
		'mc_video_url'    => 'video_url',
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
