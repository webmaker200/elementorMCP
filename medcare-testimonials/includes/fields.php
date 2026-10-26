<?php
/**
 * ACF field group, registered in code so it is version-controlled.
 *
 * @package MedCare_Testimonials
 */

defined( 'ABSPATH' ) || exit;

add_action( 'acf/include_fields', 'mc_tst_register_fields' );

/**
 * Register the Testimonial Details field group.
 */
function mc_tst_register_fields() {
	if ( ! function_exists( 'acf_add_local_field_group' ) ) {
		return;
	}

	$cta_is = static function ( $value ) {
		return array(
			array(
				array(
					'field'    => 'field_mc_cta_type',
					'operator' => '==',
					'value'    => $value,
				),
			),
		);
	};

	acf_add_local_field_group(
		array(
			'key'                   => 'group_mc_testimonial',
			'title'                 => __( 'Testimonial Details', 'medcare-testimonials' ),
			'position'              => 'acf_after_title',
			'style'                 => 'default',
			'label_placement'       => 'top',
			'instruction_placement' => 'label',
			'show_in_rest'          => 0,
			'location'              => array(
				array(
					array(
						'param'    => 'post_type',
						'operator' => '==',
						'value'    => 'mc_testimonial',
					),
				),
			),
			'fields'                => array(
				array(
					'key'          => 'field_mc_headline',
					'label'        => __( 'Headline', 'medcare-testimonials' ),
					'name'         => 'mc_headline',
					'type'         => 'text',
					'instructions' => __( 'Short word shown above the quote, e.g. "Outstanding".', 'medcare-testimonials' ),
					'maxlength'    => 40,
				),
				array(
					'key'       => 'field_mc_quote',
					'label'     => __( 'Quote', 'medcare-testimonials' ),
					'name'      => 'mc_quote',
					'type'      => 'textarea',
					'required'  => 1,
					'rows'      => 5,
					'new_lines' => '',
				),
				array(
					'key'          => 'field_mc_role',
					'label'        => __( 'Role / job title', 'medcare-testimonials' ),
					'name'         => 'mc_role',
					'type'         => 'text',
					'wrapper'      => array( 'width' => '50' ),
				),
				array(
					'key'          => 'field_mc_organization',
					'label'        => __( 'Organization', 'medcare-testimonials' ),
					'name'         => 'mc_organization',
					'type'         => 'text',
					'instructions' => __( 'Shown after the role, separated by a comma.', 'medcare-testimonials' ),
					'wrapper'      => array( 'width' => '50' ),
				),
				array(
					'key'           => 'field_mc_image',
					'label'         => __( 'Photo', 'medcare-testimonials' ),
					'name'          => 'mc_image',
					'type'          => 'image',
					'required'      => 1,
					'return_format' => 'id',
					'preview_size'  => 'medium',
					'library'       => 'all',
					'mime_types'    => 'jpg,jpeg,png,webp',
					'instructions'  => __( 'Portrait for the photo carousel (current photos are 372 × 473 px). Set the alt text in the Media Library; the person\'s name is used if it is empty.', 'medcare-testimonials' ),
					'wrapper'       => array( 'width' => '50' ),
				),
				array(
					'key'           => 'field_mc_logo',
					'label'         => __( 'Company logo (optional)', 'medcare-testimonials' ),
					'name'          => 'mc_logo',
					'type'          => 'image',
					'return_format' => 'id',
					'preview_size'  => 'medium',
					'library'       => 'all',
					'mime_types'    => 'svg,png,webp,jpg,jpeg',
					'instructions'  => __( 'Shown under the button.', 'medcare-testimonials' ),
					'wrapper'       => array( 'width' => '50' ),
				),
				array(
					'key'           => 'field_mc_cta_type',
					'label'         => __( 'Button', 'medcare-testimonials' ),
					'name'          => 'mc_cta_type',
					'type'          => 'select',
					'choices'       => array(
						'more'  => __( 'Read More (links to the Testimonials page)', 'medcare-testimonials' ),
						'video' => __( 'Watch Story (plays a video in a lightbox)', 'medcare-testimonials' ),
						'none'  => __( 'No button', 'medcare-testimonials' ),
					),
					'default_value' => 'more',
					'return_format' => 'value',
					'wrapper'       => array( 'width' => '50' ),
				),
				array(
					'key'               => 'field_mc_cta_label',
					'label'             => __( 'Button text', 'medcare-testimonials' ),
					'name'              => 'mc_cta_label',
					'type'              => 'text',
					'instructions'      => __( 'Leave empty for "Read More" / "Watch Story".', 'medcare-testimonials' ),
					'wrapper'           => array( 'width' => '50' ),
					'conditional_logic' => array(
						array(
							array(
								'field'    => 'field_mc_cta_type',
								'operator' => '!=',
								'value'    => 'none',
							),
						),
					),
				),
				array(
					'key'               => 'field_mc_video_url',
					'label'             => __( 'Video URL', 'medcare-testimonials' ),
					'name'              => 'mc_video_url',
					'type'              => 'url',
					'instructions'      => __( 'Vimeo, YouTube or a Media Library .mp4 URL.', 'medcare-testimonials' ),
					'conditional_logic' => $cta_is( 'video' ),
				),
			),
		)
	);
}

add_action( 'admin_notices', 'mc_tst_acf_notice' );

/**
 * Warn when ACF is missing, because the fields cannot be edited without it.
 */
function mc_tst_acf_notice() {
	if ( function_exists( 'acf_add_local_field_group' ) || ! current_user_can( 'activate_plugins' ) ) {
		return;
	}
	echo '<div class="notice notice-error"><p>' . esc_html__( 'MedCare Testimonials needs Advanced Custom Fields to edit testimonials.', 'medcare-testimonials' ) . '</p></div>';
}
